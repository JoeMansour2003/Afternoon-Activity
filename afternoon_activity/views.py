from django.shortcuts import render
from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Campers_Afternoon_Relation

def home(request):
    return render(request, "afternoon_activity/base/home.html")

def index(request, cabin_id):
    list_of_campers_in_cabin_x = Camper.objects.filter(cabin=cabin_id)
    return render(request, "afternoon_activity/index.html", {"list_of_campers_in_cabin_x": list_of_campers_in_cabin_x})

def cabins(request, start_cabin_id=None, end_cabin_id=None):
    if (start_cabin_id is None and end_cabin_id is None):
        list_of_cabins = Cabin.objects.all()
    if (start_cabin_id is not None and end_cabin_id is None):
        list_of_cabins = Cabin.objects.filter(cabin_number=start_cabin_id)
    else:
        list_of_cabins = Cabin.objects.filter(cabin_number__range=(start_cabin_id, end_cabin_id))
    return render(request, "afternoon_activity/cabins.html", {"list_of_cabins": list_of_cabins})