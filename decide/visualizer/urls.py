from django.urls import path
from .views import VisualizerView, Votes_csv


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('votes/<int:voting_id>/', Votes_csv.as_view()),
    path('details/<int:voting_id>', VisualizerDetails.as_view()),
    path('allCensus', VisualizerGetAllCensus.as_view()),
    path('allUsers', VisualizerGetAllUsers.as_view()),
]
