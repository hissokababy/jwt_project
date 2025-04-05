from django.urls import path

from jwtapp.views import RegisterView, UserListView

urlpatterns = [
    path('api/v1/users/', UserListView.as_view()),

    path('register/', RegisterView.as_view(), name='auth_register'),
]