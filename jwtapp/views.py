from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from jwtapp.models import User
from jwtapp.serializers import (ChangeProfilePhotoSerializer, CheckVerificationCodeSerializer, CloseAllSessionsSerializer, 
                                CloseSessionByCredentialsSerializer, CloseSessionSerializer, LoginSerializer, 
                                MySessionsSerializer, PasswordResetSerializer, RefreshTokenSerializer, 
                                RegisterSerializer, ResponseCloseSessionSerializer, ResponseLoginSerializer, ResponsePasswordResetSerializer, SetUserPasswordSerializer
                                )

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import (auth_user, close_session, close_session_by_credentials, close_sessions, 
                                    generate_user_tokens, send_code_to_user, set_user_password, set_user_photo, user_sessions, validate_code, 
                                    validate_register_data,)
from jwtapp.utils import edit_photo

from django.shortcuts import redirect
# Create your views here.

@extend_schema(tags=["Auth"], responses=ResponseLoginSerializer)
class LoginView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.values()
        
        response = auth_user(*data)

        return Response(response, status=status.HTTP_202_ACCEPTED)
    

@extend_schema(tags=["Auth"], responses=ResponseLoginSerializer)
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validate_register_data(*serializer.validated_data.values())
        
        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=["Auth"], responses=ResponseLoginSerializer)
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_tokens = generate_user_tokens(token=serializer.validated_data['refresh_token'])

        return Response(user_tokens)


@extend_schema(tags=["Auth"], responses=ResponsePasswordResetSerializer)
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = send_code_to_user(request.user, data.get('email'))

        return Response(response)
    

@extend_schema(tags=["Auth"], responses=ResponseLoginSerializer)
class CheckVerificationCodeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CheckVerificationCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        response = validate_code(user=request.user, email=data.get('email'), 
                                 verification_code=data.get('verification_code'))
        
        return Response('Please enter new password', status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=["Auth"])
class SetUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SetUserPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        response = set_user_password(user=request.user,
                                 new_password=data.get('new_password'), 
                                 confirm_password=data.get('confirm_password'))
        
        return Response('Success, please log in', status=status.HTTP_202_ACCEPTED)

# РАБОТА С СЕССИЯМИ

@extend_schema(tags=["Session"])
class MySessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MySessionsSerializer

    def get_queryset(self):
        return user_sessions(self.request.user)


@extend_schema(tags=["Session"], responses=ResponseCloseSessionSerializer)
class CloseSessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CloseSessionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = close_session(user=request.user, session_id=serializer.validated_data.get('session_id'))

        return Response(response, status=status.HTTP_202_ACCEPTED)
    

@extend_schema(tags=["Session"], responses=ResponseCloseSessionSerializer)
class CloseAllSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseAllSessionsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.values()

        response = close_sessions(*data)

        return Response(response, status=status.HTTP_202_ACCEPTED)

@extend_schema(tags=["Session"], responses=ResponseCloseSessionSerializer)
class CloseSessionByCredentialsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseSessionByCredentialsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data.values()

        response = close_session_by_credentials(*data)

        return Response(response, status=status.HTTP_202_ACCEPTED)
    

@extend_schema(tags=["Session"], responses=ResponseCloseSessionSerializer)
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
        


class ChangeProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangeProfilePhotoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo = edit_photo(*serializer.validated_data.values())
        set_user_photo(request.user, photo)

        return Response('Profile photo was set', status=status.HTTP_200_OK)