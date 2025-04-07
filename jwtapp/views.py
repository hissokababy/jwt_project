import jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from jwtapp.serializers import GetNewTokensSerializer, RegisterSerializer, UserListSerializer

from jwtapp.authentication import JWTAuthentication

from jwtapp.services.sessions import generate_user_tokens

from project_jwt.settings import TOKEN_SECRET_KEY

# Create your views here.


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def post(self, request, format=None):
        try:
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)

            user = serializer.save()
        
            response = generate_user_tokens(user)

            return Response(response, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(e)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserListSerializer



class GetNewTokensView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetNewTokensSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('refresh_token')
        
        token_validation = JWTAuthentication.validate_token(token=token)

        # token = 
        
        print(token)

        return Response('new_tokens')
        # user = User.objects.filter(username=username).first()


        # jwt_auth = JWTAuthentication()

        # jwt_token = jwt_auth.create_jwt(request, user_ip, user)

        # return Response({'JWT': jwt_token})

            