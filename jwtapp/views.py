import jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


from django.contrib.auth.models import User
from jwtapp.serializers import (CloseAllSessionsSerializer, CloseSessionByCredentialsSerializer, CloseSessionSerializer, LoginSerializer, 
                                MySessionsSerializer, PasswordResetSerializer, RefreshTokenSerializer, 
                                RegisterSerializer,
                                )

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import (auth_user, close_session, close_session_by_credentials, close_sessions, 
                                      create_user_session, generate_user_tokens, verify_phone_email)
from jwtapp.models import Session

# Create your views here.


class LoginView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        device_type = serializer.validated_data.get('device_type')
        password = serializer.validated_data.get('password')
        
        response = auth_user(email=email, password=password, device_type=device_type)

        return Response(response, status=status.HTTP_202_ACCEPTED)



class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        device_type = 'mobile'
        
        response = create_user_session(user, device_type=device_type)

        return Response(response, status=status.HTTP_201_CREATED)



class GetNewTokensView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('refresh_token')

        user_tokens = generate_user_tokens(token=token)

        return Response(user_tokens)

            
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PasswordResetSerializer


    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        send_code = serializer.validated_data.get('send_code')

        response = verify_phone_email(email=email, phone=phone, send_code=send_code)

        return Response('success')

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

        session_id = serializer.validated_data.get('session_id')

        response = close_session(session_id=session_id)

        return Response(response, status=status.HTTP_202_ACCEPTED)
    

class CloseAllSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseAllSessionsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        current_session_id = serializer.validated_data.get('current_session_id')

        response = close_sessions(current_session_id)

        return Response(response, status=status.HTTP_202_ACCEPTED)



class CloseSessionByCredentialsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseSessionByCredentialsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        session_id  = serializer.validated_data.get('session_id')
        phone  = serializer.validated_data.get('phone')
        email  = serializer.validated_data.get('email')
        password  = serializer.validated_data.get('password')

        response = close_session_by_credentials(session_id, phone, email, password)

        return Response(response, status=status.HTTP_202_ACCEPTED)



class SessionLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)

            refresh_token = serializer.validated_data.get('refresh_token')

            response = close_session(refresh_token=refresh_token)

            return Response(response, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(e)
        



