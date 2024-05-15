from django.shortcuts import render,redirect
from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Group,Session,SessionCabin,Period
import datetime

def homepage(request):
    sessions= Session.objects.all()
    return render(request, "afternoon_activity/homepage.html", {"sessions":sessions})

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
    activity_types = Period.objects.all() # Needed for NavBar
    url_session_number =  session_id # Needed for NavBar

    selected_activity=Period.objects.get(pk=activityPK)
    session_cabin = SessionCabin.objects.get(session__session_number=session_id, cabin__cabin_number=cabin_id)

    campers_in_cabin_x = Camper.objects.filter(session_cabin=session_cabin) # List of Campers {Jenny, Joe, Chris}
    
    cabin = Cabin.objects.get(cabin_number=cabin_id) # Cabin Object for that list of cabin_id {Cabin 1} 
    list_of_groups_for_that_cabin = cabin.cabins_in_group.all() # List of Groups for that Cabin {All, Seniors}
    list_of_activities_for_that_cabin = Afternoon_Activity.objects.filter(allowed_groups__in=list_of_groups_for_that_cabin, period__pk=activityPK) # List of Activities objects for all of those groups {Swimming, Archery}
    
    main_activities = None
    rainy_day_activities = None
    activity_date= None
    # POST request
    if request.method == 'POST':
        if  'activity-date' in request.POST:
            selected_date = request.POST['activity-date']
            # Convert the string to a date object
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
            # Filter the activities based on the selected date
            main_activities = list_of_activities_for_that_cabin.filter(date=selected_date, rainy_day=False)
            rainy_day_activities = list_of_activities_for_that_cabin.filter(date=selected_date, rainy_day=True)
            activity_date=selected_date
    return render(request, "afternoon_activity/Cabin.html", {"campers_in_cabin_x": campers_in_cabin_x, "main_activities": main_activities, "rainy_day_activities": rainy_day_activities, "activity_types":activity_types,"url_session_number":url_session_number,"selected_activity":selected_activity, "cabin":cabin, "activity_date":activity_date, "session_id": session_id,
    "activityPK": activityPK,
    "cabin_id": cabin_id})

def processing(request, session_id, activityPK, cabin_id):
    if request.method == 'POST':
        try:
            if 'submit_all_campers' in request.POST:
                for camper in Camper.objects.filter(session_cabin=cabin_id):
                    camper_id = request.POST.get('camper_id_' + str(camper.id))
                    activity_id = request.POST.get('activity_id_' + str(camper.id))
                    rainy_day_activity_id = request.POST.get('rainy_day_activity_id_' + str(camper.id))
                    print("#####  submit_all_campers worked #########")
                    
                    camper = Camper.objects.get(id=camper_id)
                    activity = Afternoon_Activity.objects.get(id=activity_id)
                    rainy_day_activity = Afternoon_Activity.objects.get(id=rainy_day_activity_id)
                    print(camper)
                    print(activity)
                    print(rainy_day_activity)
                    
                    activity.campers.add(camper) ## if this code is ran and camper is not already in that activity then I need to do sports available -1
                    rainy_day_activity.campers.add(camper)## if this code is ran and camper is not already in that activity then I need to do sports available -1
                    
                    activity.save()
                    rainy_day_activity.save()

            elif 'submit_one_camper' in request.POST:
                camper_id = request.POST['submit_one_camper']
                activity_id = request.POST.get('activity_id_' + str(camper_id))
                rainy_day_activity_id = request.POST.get('rainy_day_activity_id_' + str(camper_id))
                print("#####  submit_selected_campers worked #########")

                # Get the camper and activity instances
                camper = Camper.objects.get(id=camper_id)
                activity = Afternoon_Activity.objects.get(id=activity_id)
                rainy_day_activity = Afternoon_Activity.objects.get(id=rainy_day_activity_id)
                print(camper)
                print(activity)
                print(rainy_day_activity)

                # Link the camper to the activity
                activity.campers.add(camper)
                rainy_day_activity.campers.add(camper)
                print("##### Hello World #########")

                # Save the activity
                activity.save()
                rainy_day_activity.save()
                print("##### It saved #########")
            return redirect('afternoon_activity:confirmation', session_id=session_id, activityPK=activityPK, cabin_id=cabin_id)  
        except Exception:
            return redirect('afternoon_activity:error', session_id=session_id, activityPK=activityPK, cabin_id=cabin_id)  
        
          
def confirmation(request,session_id,activityPK,cabin_id):
    return render(request, "afternoon_activity/confirmation.html",{"session_id":session_id, "activityPK":activityPK ,"cabin_id":cabin_id})
def error(request,session_id,activityPK,cabin_id):
    return render(request, "afternoon_activity/error.html",{"session_id":session_id, "activityPK":activityPK ,"cabin_id":cabin_id})