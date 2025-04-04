from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
import jwt
from django.contrib.auth.models import User

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        # print(header)
        if header is None:
            return None
        
        secret_key = 'a-string-secret-at-least-256-bits-long'
        
        try:
            decoded = jwt.decode(header, secret_key, algorithms="HS256")

            # user = User.objects.filter(id=)
        except Exception as e:
            print(e)
        
        print(decoded)