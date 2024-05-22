from django.urls import path

from . import views

app_name = "afternoon_activity"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    
    path("<int:session_id>/", views.activity_selection, name="activity_selection"),
     
    path("<int:session_id>/<int:activityPK>/cabins/<int:start_cabin_id>-<int:end_cabin_id>/", views.cabins , name="cabins"), # return a list of cabins from start_cabin_id to end_cabin_id 
    path("<int:session_id>/<int:activityPK>/cabins/<int:start_cabin_id>/", views.cabins , name="cabins"), # return that 1 cabin, start_cabin_id
    path("<int:session_id>/<int:activityPK>/cabins/", views.cabins , name="cabins"), # return all cabins for that session_id
    
    path("<int:session_id>/<int:activityPK>/cabin/<int:cabin_id>/", views.cabin , name="cabin"),
    
    # path('<int:session_id>/<int:activityPK>/cabin/<int:cabin_id>/confirmation/', views.confirmation, name='confirmation'),
    # path("<int:session_id>/<int:activityPK>/cabin/<int:cabin_id>/error/", views.error , name="error"),
    # path("<int:session_id>/<int:activityPK>/cabin/<int:cabin_id>/processing/", views.processing , name="processing"),


    # path("cabin/<int:cabin_id>/<string:camper_name>", views.index , name="cabin"),
]