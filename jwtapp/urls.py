from django.urls import path

from jwtapp.views import RegisterView, UserListView, GetNewTokensView

urlpatterns = [
    path('api/v1/users/', UserListView.as_view()),

    path('register/', RegisterView.as_view(), name='auth_register'),
    path('generate_tokens/', GetNewTokensView.as_view()),
]