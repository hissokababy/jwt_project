import jwt
from jwtapp.models import Session
from django.contrib.auth.models import User

from project_jwt.settings import ALGORITHMS, TOKEN_SECRET_KEY


def create_user_session(refresh_token, user_ip):

    decoded = jwt.decode(refresh_token, TOKEN_SECRET_KEY, algorithms=ALGORITHMS)

    user_id = decoded['user_id']

    user = get_user(user_id)

    session = Session.objects.create(user=user, user_ip=user_ip, refresh_token=refresh_token)
    

def get_user(user_id):

    user = User.objects.filter(id=user_id).first()

    if user:
        return user