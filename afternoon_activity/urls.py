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
    
    path("<int:session_id>/<int:activityPK>/activity-sheet/", views.activity_sheet, name="activity_sheet"),
    
    
    path('<int:activityPK>/<str:activity_date>/', views.activity_pdf_view, name='activity_pdf'),
]