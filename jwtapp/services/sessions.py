import jwt
from jwtapp.models import Session
from django.contrib.auth.models import User

from project_jwt.settings import ACCESS_TOKEN_ALGORITHMS, TOKEN_SECRET_KEY, REFRESH_TOKEN_ALGORITHMS
from jwtapp.tokens import generate_access_token, generate_refresh_token


def create_user_session(user, device_type):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_session = Session.objects.create(user=user, refresh_token=refresh_token, device_type=device_type)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response


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
        
    session = Session.objects.get(refresh_token=token)

    if session.user.is_active and session.active == True:

        access_token = generate_access_token(session.user)
        refresh_token = generate_refresh_token(session.user)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        session.refresh_token = refresh_token
        session.save()
    
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



def close_session_by_credentials(session_id, phone, email, password):
    
    session = Session.objects.get(pk=session_id)

    verified = session.user.check_password(raw_password=password)

    if verified is False:
        return None
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response


def auth_user(email, password, device_type):
    user = User.objects.get(email=email)
    verified = user.check_password(raw_password=password)

    if verified is False:
        return None
    
    session_saved = None

    for session in user.sessions.all():
        if session.device_type == device_type:
            session.active = True

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            session.refresh_token = refresh_token
            session.save()
            session_saved = True
    
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        

    if not session_saved:
        response = create_user_session(user, device_type=device_type)
    
    return response


def verify_phone_email(phone, email, send_code):

    user = User.objects.filter(email=email).first()

    if user and send_code is False:
        
        ...

    return True

