import jwt
from django.utils import timezone

from project_jwt.settings import (ALGORITHMS, 
                                  ACCESS_TOKEN_EXPIRE, ACCESS_TOKEN_SECRET_KEY, 
                                  REFRESH_TOKEN_EXPIRE, REFRESH_TOKEN_SECRET_KEY,
                                  HS256_ALGORITHM, RS256_ALGORITHM,
                                  PUBLIC_KEY, PRIVATE_KEY)


def generate_access_token(user):

    payload = {
        'user_id': user.id,
        'exp': timezone.now().timestamp() + ACCESS_TOKEN_EXPIRE,
        'iat': timezone.now().timestamp(),
    }

    if ALGORITHMS == HS256_ALGORITHM:
        access_token = jwt.encode(payload=payload, key=ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHMS)
    
    elif ALGORITHMS == RS256_ALGORITHM:
        access_token = jwt.encode(payload=payload, key=PRIVATE_KEY, algorithm=ALGORITHMS)

    return access_token


def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'name': f'{user.username}',
        'exp': timezone.now().timestamp() + REFRESH_TOKEN_EXPIRE,
        'iat': timezone.now().timestamp(),
    }

    if ALGORITHMS == HS256_ALGORITHM:
        refresh_token = jwt.encode(payload=payload, key=REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHMS)
    
    elif ALGORITHMS == RS256_ALGORITHM:
        refresh_token = jwt.encode(payload=payload, key=PRIVATE_KEY, algorithm=ALGORITHMS)

    return refresh_token


def decode_access_token(access_token):
    try:
        if ALGORITHMS == HS256_ALGORITHM:
            decoded = jwt.decode(access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHMS)
        elif ALGORITHMS == RS256_ALGORITHM:
            decoded = jwt.decode(access_token, PUBLIC_KEY, algorithms=ALGORITHMS)

        return decoded
    except Exception as e:
        raise jwt.exceptions.DecodeError(e)


def decode_refresh_token(refresh_token):
    try:
        if ALGORITHMS == HS256_ALGORITHM:
            decoded = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=ALGORITHMS)
        elif ALGORITHMS == RS256_ALGORITHM:
            decoded = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=ALGORITHMS)
        
        return decoded

    except Exception as e:
        raise jwt.exceptions.DecodeError(e)


