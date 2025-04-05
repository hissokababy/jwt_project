import jwt
import time
from rest_framework import response
from django.utils import timezone
from jwtapp.services.sessions import get_user

from project_jwt.settings import ACCESS_TOKEN_EXPIRE, TOKEN_SECRET_KEY

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': time.time() + ACCESS_TOKEN_EXPIRE,
        'iat': time.time(),
    }
    timezone.now().timestamp()
    access_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm="HS256")

    return access_token


def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': time.time() + (7 * 86400),
        'iat': time.time(),
    }
    refresh_token = jwt.encode(payload=payload, key=TOKEN_SECRET_KEY, algorithm="HS256")

    return refresh_token


def handle_token(user):
    user = get_user(user)

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)



