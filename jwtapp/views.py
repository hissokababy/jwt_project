import jwt
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.models import User
from jwtapp.serializers import RegisterSerializer, UserListSerializer
from jwtapp.authentication import JWTAuthentication

from jwtapp.services.tokens import generate_access_token, generate_refresh_token, set_jwt_cookies
from jwtapp.configs import SECRET_KEY
from jwtapp.services.sessions import user_sessions

# Create your views here.


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
        
            user = User.objects.get(id=user.id)

            if user and user.is_active == True:

                access_token = generate_access_token(user.id)
                refresh_token = generate_refresh_token(user.id)

                user_sessions(user, token=refresh_token)

                response = Response('SUCCESS REGIST', status=status.HTTP_201_CREATED)

                response_cookies = set_jwt_cookies(response, access_token=access_token, refresh_token=refresh_token)
                return response_cookies

            return response.Response('OK', status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    authentication_classes = [JWTAuthentication]

    

