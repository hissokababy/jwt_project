from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from jwtapp.models import User
from jwtapp.serializers import (CheckVerificationCodeSerializer, CloseAllSessionsSerializer, 
                                CloseSessionByCredentialsSerializer, CloseSessionSerializer, LoginSerializer, 
                                MySessionsSerializer, PasswordResetSerializer, RefreshTokenSerializer, 
                                RegisterSerializer,
                                )

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import (auth_user, close_session, close_session_by_credentials, close_sessions, 
                                    generate_user_tokens, send_code_to_user, user_sessions, validate_code, validate_refresh_token, 
                                    validate_register_data, validate_session_id, verify_phone_email)

# Create your views here.

@extend_schema(tags=["Auth"])
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

@extend_schema(tags=["Auth"])
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        response = validate_register_data(serializer.validated_data)
        
        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.values()
        
        token = validate_refresh_token(*data)

        user_tokens = generate_user_tokens(token=token)

        return Response(user_tokens)

@extend_schema(tags=["Auth"])
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.values()

        user = verify_phone_email(*data)

        response = send_code_to_user(user)

        return Response(response)

@extend_schema(tags=["Auth"])
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

@extend_schema(tags=["Session"])
class CloseSessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CloseSessionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.values()

        session = validate_session_id(*data)

        response = close_session(session_id=session.id)

        return Response(response, status=status.HTTP_202_ACCEPTED)
    
@extend_schema(tags=["Session"])
class CloseAllSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseAllSessionsSerializer

    @extend_schema(tags=["Session"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.values()
        current_session = validate_session_id(*data)

        response = close_sessions(current_session.id)

        return Response(response, status=status.HTTP_202_ACCEPTED)

@extend_schema(tags=["Session"])
class CloseSessionByCredentialsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CloseSessionByCredentialsSerializer

    @extend_schema(tags=["Session"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_session_id(serializer.validated_data['session_id'])
        data = serializer.validated_data.values()

        response = close_session_by_credentials(*data)

        return Response(response, status=status.HTTP_202_ACCEPTED)

@extend_schema(tags=["Session"])
class SessionLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer

    @extend_schema(tags=["Session"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data.get('refresh_token')

            response = close_session(refresh_token=refresh_token)

            return Response(response, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(e)
        

