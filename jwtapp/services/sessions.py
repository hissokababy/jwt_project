import jwt
from jwtapp.models import Session
from django.contrib.auth.models import User

from project_jwt.settings import ACCESS_TOKEN_ALGORITHMS, TOKEN_SECRET_KEY, REFRESH_TOKEN_ALGORITHMS
from jwtapp.tokens import generate_access_token, generate_refresh_token


def create_user_session(refresh_token, user_ip):

    decoded = jwt.decode(refresh_token, TOKEN_SECRET_KEY, algorithms=REFRESH_TOKEN_ALGORITHMS)

    user_id = decoded['user_id']

    user = get_user(user_id)

    session = Session.objects.create(user=user, user_ip=user_ip, refresh_token=refresh_token)
    

def get_user(user_id):

    user = User.objects.filter(id=user_id).first()

    if user:
        return user
    


def create_user(validated_data):

    user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
    user.set_password(validated_data['password'])
    user.save()
    return user




def generate_user_tokens(user):
    user = User.objects.get(id=user.id)

    if user and user.is_active == True:

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        create_user_session(refresh_token)
    
    return response