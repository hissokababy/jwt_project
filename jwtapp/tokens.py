import jwt
import time
from rest_framework import response
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


from jwtapp.services.sessions import get_user

from jwtapp.models import Session
from project_jwt.settings import ACCESS_TOKEN_EXPIRE, TOKEN_SECRET_KEY

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': time.time() + ACCESS_TOKEN_EXPIRE,
        'iat': time.time(),
    }
    timezone.now().timestamp()
    access_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm="HS256")

    return access_token


def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'name': f'{user.username}',
        'exp': time.time() + (7 * 86400),
        'iat': time.time(),
    }
    refresh_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm="HS256")

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



