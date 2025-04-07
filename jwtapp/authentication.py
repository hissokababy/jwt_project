import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

from jwt import exceptions
from project_jwt.settings import TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHMS, REFRESH_TOKEN_ALGORITHMS
from jwtapp.tokens import update_token
from jwtapp.models import Session


class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if header is None:
            return None

        token = header

        token = self.get_raw_token(token)

        if token is None:
            return None


        user = self.validate_token(token)

        self.check_user_ip(request, user, token)

        return (user, None)
    

    def get_raw_token(self, header):

        parts = header.split()

        if len(parts) == 0:
            return None

        return parts[0]



    def check_user_ip(self, request, user, token):
        # current_ip = get_client_ip(request)
        current_ip = '127.0.0.2'

        user_sessions = Session.objects.filter(user=user)

        user_ips = [i.user_ip for i in user_sessions]

        if not current_ip in user_ips and not len(user_ips) <= 3:
            session = Session.objects.create(user=user, user_id=current_ip, refresh_token=token)
            session.save()

        print(user_ips)
        # print(session)


    def validate_token(self, token):
        try:
            decoded = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=ACCESS_TOKEN_ALGORITHMS)

            user_id = decoded['user_id']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed(exceptions.ExpiredSignatureError.__name__)
        
        except Exception as e:
            raise AuthenticationFailed(e)
        
        return user