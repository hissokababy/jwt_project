import jwt
from datetime import datetime, timedelta
from rest_framework import response

from jwtapp.configs import SECRET_KEY


def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(minutes=5),
        'iat': datetime.now(),
    }
    access_token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

    return access_token


def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(days=7),
        'iat': datetime.now(),
    }
    refresh_token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

    return refresh_token


def set_jwt_cookies(response: response.Response, access_token: str, refresh_token: str) -> response.Response:
    response.set_cookie(
        'access_token',
        access_token,
        httponly=True,
        # secure=True,
        samesite='strict'
    )
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        # secure=True,
        samesite='strict'
    )

    return response
