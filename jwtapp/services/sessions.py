import jwt
from jwtapp.models import Session
from django.contrib.auth.models import User

from project_jwt.settings import ACCESS_TOKEN_ALGORITHMS, TOKEN_SECRET_KEY, REFRESH_TOKEN_ALGORITHMS
from jwtapp.tokens import generate_access_token, generate_refresh_token


def create_user_session(refresh_token):

    decoded = jwt.decode(refresh_token, TOKEN_SECRET_KEY, algorithms=REFRESH_TOKEN_ALGORITHMS)

    user_id = decoded['user_id']

    user = get_user(user_id)

    session = Session.objects.filter(user=user).first()

    if session and session.active == True:
        session.refresh_token = refresh_token
    else:
        session = Session.objects.create(user=user, refresh_token=refresh_token)

    session.save()

    

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



def generate_user_tokens(token):
        
    decoded = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=ACCESS_TOKEN_ALGORITHMS)

    user_id = decoded['user_id']

    user = get_user(user_id)

    if user and user.is_active == True:

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        create_user_session(refresh_token)
    
    return response


def generate_new_user_tokens(user):

    user = get_user(user.id)

    if user and user.is_active == True:

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        create_user_session(refresh_token)
    
    return response



def validate_closing_session(session_id):
    sessions = [i.pk for i in Session.objects.all()]

    if session_id in sessions:
        return True


def close_session(session_id=None, refresh_token=None):

    if session_id:
        session = Session.objects.get(pk=session_id)
    elif refresh_token:
        session = Session.objects.get(refresh_token=refresh_token)

    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}

    return response


def close_sessions(current_session_id):

    user_sessions = [i for i in Session.objects.get(pk=current_session_id).user.sessions.all()]

    for session_id in user_sessions:
        if session_id.pk != current_session_id:
            session_id.active = False
        
        session_id.save()
    
    response = {
        "results": {"closed": True}}

    return response


def auth_user(request, email, password, device_type):
    user = User.objects.get(email=email)
    verified = user.check_password(raw_password=password)

    if verified is False:
        return None
    
    for session in user.sessions.all():
        if session.device_type == device_type:
            session.active = True
            session.save()

        else:
            generate_new_user_tokens(user)
    ...