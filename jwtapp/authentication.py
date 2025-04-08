import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

from jwt import exceptions
from jwtapp.tokens import validate_token
from project_jwt.settings import TOKEN_AUTH_HEADER
from jwtapp.services.sessions import get_user


class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        # header = request.headers
        # print(header)
        header = request.headers.get("Authorization")

        if header is None:
            return None
        
        token = self.get_raw_token(header)

        if token is None:
            return None

        user = self.validate_token_auth(token)

        return (user, None)
    

    def get_raw_token(self, header):

        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0] != TOKEN_AUTH_HEADER:
            return None

        return parts[1]
        # return parts[0]


    def validate_token_auth(self, token):
        user = validate_token(token)
        return user