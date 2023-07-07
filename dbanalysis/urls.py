from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.TicketView.as_view()),
    path('sprints/', views.SprintView.as_view()),
    path('channels/', views.ChannelView.as_view()),
    path('messages/', views.MessageView.as_view()),
    path('mentions/', views.MentionView.as_view()),
    path('documents/', views.DocumentView.as_view()),
    path('pull-requests/', views.PullRequestsView.as_view()),
    path('prequest-reviewers/', views.PullRequestReviewersView.as_view()),
    path('batch-logs/', views.BatchLogView.as_view()),
    path('developers/', views.DevelopersView.as_view()),
]