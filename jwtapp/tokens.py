import jwt
import time
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


from jwtapp.models import Session
from project_jwt.settings import (ACCESS_TOKEN_ALGORITHMS, 
                                  ACCESS_TOKEN_EXPIRE, TOKEN_SECRET_KEY, 
                                  REFRESH_TOKEN_EXPIRE, REFRESH_TOKEN_ALGORITHMS)


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': time.time() + ACCESS_TOKEN_EXPIRE,
        'iat': time.time(),
    }
    timezone.now().timestamp()
    access_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHMS)

    return access_token


def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'name': f'{user.username}',
        'exp': time.time() + REFRESH_TOKEN_EXPIRE,
        'iat': time.time(),
    }
    refresh_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm=REFRESH_TOKEN_ALGORITHMS)

    return refresh_token


def update_token(user_ip, user, token):

    session = Session.objects.get(user=user, user_ip=user_ip)

    if not token == session.refresh_token:
        raise AuthenticationFailed('invalid token')

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    session.refresh_token = refresh_token
    session.save()

    response = {
        'access': access_token,
        'refresh': refresh_token
    }

    return response





def create_jwt(request, user_ip, user):
    header = request.headers.get("Authorization")

    parts = header.split()
    if len(parts) == 0:
        return None
    
    jwt_token = update_token(user_ip, user, header)
    return jwt_token