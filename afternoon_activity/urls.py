from django.urls import path

from . import views

app_name = "afternoon_activity"
urlpatterns = [
    path("", views.index, name="index"),
    path("cabin/<int:cabin_id>/", views.index , name="cabin"),
    # path("cabin/<int:cabin_id>/<string:camper_name>", views.index , name="cabin"),
]