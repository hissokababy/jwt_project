from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.models import User
from jwtapp.serializers import UserListSerializer
from jwtapp.authentication import JWTAuthentication

# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    authentication_classes = [JWTAuthentication]
