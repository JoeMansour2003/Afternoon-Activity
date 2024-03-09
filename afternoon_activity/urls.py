from django.urls import path

from . import views

app_name = "afternoon_activity"
urlpatterns = [
    path("", views.index, name="index"),
]