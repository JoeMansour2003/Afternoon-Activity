from django.shortcuts import render
from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Campers_Afternoon_Relation,Group,Session,SessionCabin,Period

def home(request):
    return render(request, "afternoon_activity/base/home.html")

def cabin(request, cabin_id):
    campers_in_cabin_x = Camper.objects.filter(session_cabin=cabin_id) # List of Campers {Jenny, Joe, Chris}
    
    cabin = Cabin.objects.get(cabin_number=cabin_id) # Cabin Object for that list of cabin_id {Cabin 1} 
    list_of_groups_for_that_cabin = cabin.cabins_in_group.all() # List of Groups for that Cabin {All, Seniors}
    list_of_activities_for_that_cabin = Afternoon_Activity.objects.filter(allowed_groups__in=list_of_groups_for_that_cabin) # List of Activities objects for all of those groups {Swimming, Archery}
    
    first_period_activities = list_of_activities_for_that_cabin.filter(second_period=False)
    second_period_activities = list_of_activities_for_that_cabin.filter(second_period=True)

    return render(request, "afternoon_activity/cabin.html", {"campers_in_cabin_x": campers_in_cabin_x, "first_period_activities": first_period_activities, "second_period_activities": second_period_activities})

def cabins(request, start_cabin_id=None, end_cabin_id=None):
    if (start_cabin_id is None and end_cabin_id is None):
        list_of_cabins = Cabin.objects.all() # Does not work but it's okay I found another work around.
    if (start_cabin_id is not None and end_cabin_id is None):
        list_of_cabins = Cabin.objects.filter(cabin_number=start_cabin_id)
    else:
        list_of_cabins = Cabin.objects.filter(cabin_number__range=(start_cabin_id, end_cabin_id))
    return render(request, "afternoon_activity/cabins.html", {"list_of_cabins": list_of_cabins})

