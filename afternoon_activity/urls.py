from django.urls import path

from . import views

app_name = "afternoon_activity"
urlpatterns = [
    path("", views.home, name="homepage"),
    
    path("cabin/<int:session_id>/<int:cabin_id>/", views.cabin , name="cabin"),
    
    path("cabins/<int:session_id>/<int:start_cabin_id>-<int:end_cabin_id>/", views.cabins , name="cabins"),
    path("cabins/<int:session_id>/<int:start_cabin_id>/", views.cabins , name="cabins"),
    path("cabins/<int:session_id>/", views.cabins , name="cabins"),
    path("cabins/", views.cabins , name="cabins"),
    
    # path("cabin/<int:cabin_id>/<string:camper_name>", views.index , name="cabin"),
]