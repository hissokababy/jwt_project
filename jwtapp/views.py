import jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


from django.contrib.auth.models import User
from jwtapp.serializers import (CloseSessionSerializer, MySessionsSerializer, RefreshTokenSerializer, 
                                RegisterSerializer,
                                )

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import generate_new_user_tokens, generate_user_tokens
from jwtapp.models import Session

# Create your views here.


class LoginView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)


                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)

            user = serializer.save()
        
            response = generate_new_user_tokens(user)

            return Response(response, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(e)


class GetNewTokensView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('refresh_token')

        user_tokens = generate_user_tokens(token=token)

        return Response(user_tokens)

            

# РАБОТА С СЕССИЯМИ

class MySessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MySessionsSerializer

    def get_queryset(self):
        return Session.objects.filter(user=self.request.user)


class CloseSessionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseSessionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        print(serializer)

        return Response('1', status=status.HTTP_201_CREATED)











class SessionLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)

            print(serializer)

            return Response('1', status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(e)
        



