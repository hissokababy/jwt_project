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
                                RegisterSerializer, ResponseCloseSessionSerializer, ResponseLoginSerializer, ResponsePasswordResetSerializer
                                )

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import (auth_user, close_session, close_session_by_credentials, close_sessions, 
                                    generate_user_tokens, send_code_to_user, user_sessions, validate_code, 
                                    validate_register_data,)
from jwtapp.utils import change_user_photo

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
        
        response = validate_register_data(serializer.validated_data)
        
        return Response(response, status=status.HTTP_201_CREATED)


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
        data = serializer.validated_data.values()

        response = send_code_to_user(*data)

        return Response(response)

@extend_schema(tags=["Auth"], responses=ResponseLoginSerializer)
class CheckVerificationCodeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CheckVerificationCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.values()
        
        response = validate_code(*data)
        return Response(response)



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

        response = close_session(session_id=serializer.validated_data['session_id'])

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

        change_user_photo(*serializer.validated_data.values())
        return Response(status=status.HTTP_200_OK)