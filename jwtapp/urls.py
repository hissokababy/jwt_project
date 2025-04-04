from django.urls import path

from jwtapp.views import UserListView

urlpatterns = [
    path('api/v1/users/', UserListView.as_view())

]