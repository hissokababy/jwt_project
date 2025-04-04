from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User


from jwtapp.serializers import UserSerializer

# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
