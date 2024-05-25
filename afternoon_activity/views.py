import pprint
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from .models import ProgramActivity,Activity,Camper,Cabin,Counselor,Group,Session,SessionCabin,Period
import datetime, requests, os
from dotenv import load_dotenv


def homepage(request):
    sessions= Session.objects.all()
    List_of_activities = Period.objects.all()
    return render(request, "afternoon_activity/homepage.html", {"sessions":sessions,"List_of_activities":List_of_activities})

def activity_selection(request, session_id):
    session = Session.objects.get(session_number=session_id)
    url_session_number = session_id
    activity_types = Period.objects.all()
    return render(request, "afternoon_activity/activity_selection.html", {"session" : session ,"activity_types": activity_types,"url_session_number":url_session_number})


def cabins(request, session_id, activityPK, start_cabin_id=None, end_cabin_id=None):
    activity_types = Period.objects.all() # Needed for NavBar
    url_session_number =  session_id # Needed for NavBar
    
    # url_activityPK =  activityPK # Needed for NavBar
    
    activity_type_pks = list(Period.objects.values_list('pk', flat=True)) # Used to check if the current activityPK is valid


    selected_activity=Period.objects.get(pk=activityPK)
    # Filter SessionCabin objects by session_id
    session_cabins = SessionCabin.objects.filter(session__session_number=session_id)
    
    # If start_cabin_id is given
    if start_cabin_id is not None:
        # If end_cabin_id is also given, get cabins in range
        if end_cabin_id is not None: 
            session_cabins = session_cabins.filter(cabin__cabin_number__range=(start_cabin_id, end_cabin_id))
        # If only start_cabin_id is given, get that one cabin
        else:
            session_cabins = session_cabins.filter(cabin__cabin_number=start_cabin_id)

    # Extract Cabin objects from SessionCabin objects
    list_of_cabins = [sc.cabin for sc in session_cabins]
    
    for cabin in list_of_cabins:
        cabin.counselors = [{'first_name': counselor[0], 'last_name': counselor[1]} for counselor in SessionCabin.objects.filter(session__session_number=session_id, cabin=cabin).values_list('counselors_for_session_cabin__first_name', 'counselors_for_session_cabin__last_name')]

    
    return render(request, "afternoon_activity/Cabins.html", {"list_of_cabins": list_of_cabins, "session_cabins": session_cabins, "activityPK": activityPK, "activity_types": activity_types,"activity_type_pks": activity_type_pks, "url_session_number":url_session_number,"selected_activity":selected_activity})



def cabin(request, session_id, activityPK, cabin_id):

    tomorrows_weather_data = get_tomorrows_weather_data()
    tomorrows_weather = round(tomorrows_weather_data["main"]["feels_like"] - 273.15,1)
    tomorrows_rain = tomorrows_weather_data["rain"]["3h"] if "rain" in tomorrows_weather_data and "3h" in tomorrows_weather_data["rain"] else 0
    tomorrows_icon = tomorrows_weather_data["weather"][0]["icon"]
    tomorrows_description = tomorrows_weather_data["weather"][0]["description"]
    
    activity_types = Period.objects.all() # Needed for NavBar
    url_session_number =  session_id # Needed for NavBar

    selected_activity=Period.objects.get(pk=activityPK)
    session_cabin = SessionCabin.objects.get(session__session_number=session_id, cabin__cabin_number=cabin_id)

    campers_in_cabin_x = Camper.objects.filter(session_cabin=session_cabin) # List of Campers {Jenny, Joe, Chris}
    
    cabin = Cabin.objects.get(cabin_number=cabin_id) # Cabin Object for that list of cabin_id {Cabin 1} 
    list_of_groups_for_that_cabin = cabin.cabins_in_group.all() # List of Groups for that Cabin {All, Seniors}
    list_of_activities_for_that_cabin = ProgramActivity.objects.filter(allowed_groups__in=list_of_groups_for_that_cabin, period__pk=activityPK) # List of Activities objects for all of those groups {Swimming, Archery}
    
    periods = ["First Period", "Second Period"]

    main_activities = None
    rainy_day_activities = None
    activity_date= None
    # POST request
    if request.method == 'POST':
        if 'submit_all_campers' in request.POST:
            for camper in Camper.objects.filter(session_cabin=cabin_id):
                camper_id = request.POST.get('camper_id_' + str(camper.id))
                activity_id = request.POST.get('activity_id_' + str(camper.id))
                rainy_day_activity_id = request.POST.get('rainy_day_activity_id_' + str(camper.id))
                selected_date = request.POST.get('activity-date', None)

                print("#####  submit_all_campers worked #########")
                
                camper = Camper.objects.get(id=camper_id)
                activities_camper_is_currently_enrolled=camper.camper_in_activity.filter(period=activityPK,date=selected_date)

                print(camper)
                # print(activity)
                print(rainy_day_activity_id)
                

                for previous_activity in activities_camper_is_currently_enrolled:
                    previous_activity.campers.remove(camper)
                    previous_activity.spots_left += 1
                    previous_activity.save()
                    print("we removed the camper from the old activity")
                    
                    
                if (activity_id is not None):
                    activity = ProgramActivity.objects.get(id=activity_id)
                    activity.campers.add(camper)
                    activity.spots_left -= 1
                    activity.save()
                    print("### Activity Saved ###")
                
                if (rainy_day_activity_id is not None):
                    rainy_day_activity = ProgramActivity.objects.get(id=rainy_day_activity_id)
                    rainy_day_activity.campers.add(camper)
                    rainy_day_activity.spots_left -= 1
                    rainy_day_activity.save()
                    print("### Rainy Day Activity Saved ###")
        elif 'submit_one_camper' in request.POST:
            camper_id = request.POST['submit_one_camper']
            activity_id = request.POST.get('activity_id_' + str(camper_id))
            rainy_day_activity_id = request.POST.get('rainy_day_activity_id_' + str(camper_id))
            print("#####  submit_selected_campers worked #########")

            # Get the camper and activity instances
            camper = Camper.objects.get(id=camper_id)
            all_activity = ProgramActivity.objects.all()
            selected_date = request.POST.get('activity-date', None)
            activities_camper_is_currently_enrolled=camper.camper_in_activity.filter(period_id=activityPK,date=selected_date)
            print(camper)
            pprint.pp(all_activity)
            print("##########################")
            pprint.pp(camper.camper_in_activity.all())
            pprint.pp(camper.camper_in_activity.filter(period_id=activityPK,date=selected_date))
            print("##########################")
        
            for previous_activity in activities_camper_is_currently_enrolled:
                previous_activity.campers.remove(camper)
                previous_activity.spots_left += 1
                previous_activity.save()
                print("we removed the camper from the activity")
                
            if (activity_id is not None):
                activity = ProgramActivity.objects.get(id=activity_id)
                activity.campers.add(camper)
                activity.spots_left -= 1
                activity.save()
                print("### Activity Saved ###")
                
            if rainy_day_activity_id is not None:
                rainy_day_activity = ProgramActivity.objects.get(id=rainy_day_activity_id)
                rainy_day_activity.campers.add(camper)
                rainy_day_activity.spots_left -= 1
                rainy_day_activity.save()
                print("### Rainy Day Activity Saved ###")
            
            # Link the camper to the activity
            if (activity_id is not None):
                try:
                    activity.campers.add(camper)
                    activity.spots_left -= 1
                except ValueError as e:
                    print(e)
                    return JsonResponse({'error': '1 or more camper tried to book an activity that is full. Please choose another activity. Your entry failed to save.'})
                except Exception as e:
                    print(e)
                    return JsonResponse({'error': 'An error occurred. Your entry failed to save.'})


            print("##### Hello World #########")
            
            
        
        if 'activity-date' in request.POST or 'submit_all_campers' in request.POST or 'submit_one_camper' in request.POST:
            selected_date = request.POST.get('activity-date', None)
            if selected_date is not None:
                # Convert the string to a date object
                selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
                # Filter the activities based on the selected date
                main_activities = list_of_activities_for_that_cabin.filter(date=selected_date, rainy_day=False)
                rainy_day_activities = list_of_activities_for_that_cabin.filter(date=selected_date, rainy_day=True)
                activity_date=selected_date
    return render(request, "afternoon_activity/Cabin.html", {"campers_in_cabin_x": campers_in_cabin_x, "main_activities": main_activities, "rainy_day_activities": rainy_day_activities, "activity_types":activity_types,"url_session_number":url_session_number,"selected_activity":selected_activity, "cabin":cabin, "activity_date":activity_date, "session_id": session_id,
    "activityPK": activityPK,
    "cabin_id": cabin_id,
    "list_of_activities_for_that_cabin":list_of_activities_for_that_cabin,
    "periods":periods,
    "tomorrows_weather":tomorrows_weather,
    "tomorrows_rain":tomorrows_rain,
    "tomorrows_icon":tomorrows_icon,
    "tomorrows_description":tomorrows_description})
    
def get_tomorrows_weather_data():
    load_dotenv()
    lat = os.getenv("lat")
    lon = os.getenv("lon")
    api_key = os.getenv("OPENWEATHERMAP_API_KEY2")

    # Make a GET request to the OpenWeatherMap API
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}")

    # Convert the response to JSON
    data = response.json()

    # Get the weather data for tomorrow
    tomorrow_data = data['list'][1]

    return tomorrow_data
def activity_sheet(request, session_id, activityPK):
    activity_types = Period.objects.all() # Needed for NavBar
    url_session_number =  session_id # Needed for NavBar
    url_activityPK =  activityPK
    session_cabins = SessionCabin.objects.filter(session__session_number=session_id)
    # list_of_cabins = [sc.cabin for sc in session_cabins]
    current_date = timezone.now().date().strftime('%Y-%m-%d')
    activities = []

    if request.method == 'POST':
        selected_date = request.POST.get('activity-date')
        if selected_date:  # Check if selected_date is not an empty string
            selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
            activities = ProgramActivity.objects.filter(date=selected_date, period=selected_period)
            campers = [activity.campers.all() for activity in activities]
        else:
            selected_date = timezone.datetime.strptime(current_date, '%Y-%m-%d').date()
            activities = ProgramActivity.objects.filter(date=selected_date, period=selected_period)
            campers = [activity.campers.all() for activity in activities]

    else:
        campers = []

    return render(request, "afternoon_activity/activity_sheet.html", {"session_cabins": session_cabins, "activityPK": activityPK, "activity_types": activity_types,"url_session_number":url_session_number,"selected_period":selected_period, "campers": campers, "current_date": current_date, "url_activityPK": url_activityPK, "activities":activities})