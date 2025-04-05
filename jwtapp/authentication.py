import jwt
from rest_framework.authentication import BaseAuthentication

from jwtapp.configs import SECRET_KEY

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        # print(header)
        if header is None:
            return None
        
        try:
            decoded = jwt.decode(header, SECRET_KEY, algorithms="HS256")

            # user = User.objects.filter(id=)
            print(decoded)
        except Exception as e:
            print(e)
        