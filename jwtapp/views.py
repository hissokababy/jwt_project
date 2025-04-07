import jwt
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from jwtapp.serializers import GetNewTokensSerializer, RegisterSerializer, UserListSerializer

from jwtapp.authentication import JWTAuthentication

from jwtapp.tokens import generate_access_token, generate_refresh_token
from jwtapp.services.sessions import create_user_session

from jwtapp.utils import get_client_ip
from project_jwt.settings import TOKEN_SECRET_KEY

# Create your views here.


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        
        user_ip = get_client_ip(request)
        
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
        
            user = User.objects.get(id=user.id)

            if user and user.is_active == True:

                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)

                response = {
                    'access': access_token,
                    'refresh': refresh_token
                }

                create_user_session(refresh_token, user_ip)

                return Response(response, status=status.HTTP_201_CREATED)


            return Response('OK', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserListSerializer



class GetNewTokensView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetNewTokensSerializer

    def post(self, request, *args, **kwargs):

        user_ip = get_client_ip(request)

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')

        user = User.objects.filter(username=username).first()

        print(user)

        if user is None:
            return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
        
        jwt_auth = JWTAuthentication()

        jwt_token = jwt_auth.create_jwt(request, user_ip, user)

        return Response({'JWT': jwt_token})

            