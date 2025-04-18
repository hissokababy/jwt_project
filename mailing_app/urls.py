from django.urls import path

from mailing_app.views import TaskDetailView


urlpatterns = [
    path('api/v1/mailing/task/<int:pk>/', TaskDetailView.as_view()),

]