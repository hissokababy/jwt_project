import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from jwtapp.services.sessions import update_token
from project_jwt.settings import TOKEN_SECRET_KEY

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        # header = request.headers.get("Authorization")

        header = request.headers

        if header is None:
            return None
        
        try:
            header = request.headers['Cookie']
        except:
            return None
        
        access_token, refresh_token = header.split('; ')

        if access_token.startswith('access_token') and refresh_token.startswith('refresh_token'):

            access_token = access_token.split('=')[-1]
            refresh_token = refresh_token.split('=')[-1]

        try:
            decoded = jwt.decode(access_token, TOKEN_SECRET_KEY, algorithms="HS256")
            
            # update_token()

        except Exception as e:
            raise AuthenticationFailed(e)
            
        