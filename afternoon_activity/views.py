from django.shortcuts import render
from .models import Afternoon_Activity,Activity,Camper,Cabin,Counselor,Campers_Afternoon_Relation

def home(request):
    return render(request, "afternoon_activity/home.html")

def index(request, cabin_id):
    list_of_campers_in_cabin_x = Camper.objects.filter(cabin=cabin_id)
    return render(request, "afternoon_activity/index.html", {"list_of_campers_in_cabin_x": list_of_campers_in_cabin_x})
