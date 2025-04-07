import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

from jwt import exceptions
from project_jwt.settings import TOKEN_SECRET_KEY, ALGORITHMS
from jwtapp.services.sessions import get_user
from jwtapp.tokens import update_token

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if header is None:
            return None
        
        token = header

        token = self.get_raw_token(token)

        if token is None:
            return None

        try:
            decoded = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=ALGORITHMS)

            user_id = decoded['user_id']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed(exceptions.ExpiredSignatureError.__name__)
        
        except Exception as e:
            raise AuthenticationFailed(e)
        
        return (user, None)
    

    def get_raw_token(self, header):

        parts = header.split()

        if len(parts) == 0:
            return None

        return parts[0]
    

    def create_jwt(self, request, user_ip, user):
        header = request.headers.get("Authorization")
        token = self.get_raw_token(header)

        jwt_token = update_token(user_ip, user, token)
        return jwt_token
