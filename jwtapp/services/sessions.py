import random
from jwtapp.models import Session
from django.utils import timezone

from jwtapp.utils import send_user_message

from jwtapp.tokens import decode_access_token, decode_refresh_token, generate_access_token, generate_refresh_token

from rest_framework import serializers

from jwtapp.models import Session, User
from jwtapp.exeptions import NoUserExists, InvalidSessionExeption



def generate_user_tokens(token):
    decoded = decode_refresh_token(token)
    
    user = get_user(decoded['user_id'])

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    create_user_session(user, refresh_token)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return response


def close_session(user=None, session_id=None, refresh_token=None):
    user = get_user(user.id)

    if session_id:
        try:
            session = Session.objects.get(pk=session_id, user=user)
        except Session.DoesNotExist:
            raise InvalidSessionExeption('Session does not exist')

    elif refresh_token:
        try:
            session = Session.objects.get(refresh_token=refresh_token, user=user)
        except Session.DoesNotExist:
            raise InvalidSessionExeption('Session does not exist')
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response
    


def close_sessions(user, current_session_id):
    user = get_user(user.id)

    try:
        current_session = Session.objects.get(pk=current_session_id, user=user)
    except Session.DoesNotExist:
        raise InvalidSessionExeption('Session does not exist')

    if not current_session.active:
        raise InvalidSessionExeption
    
    user_sessions = Session.objects.filter(user=user, active=True).exclude(pk=current_session.id)

    sessions = []

    for session in user_sessions:
        session.active = False
        sessions.append(session)

    updated = Session.objects.bulk_update(sessions, fields=['active'])
    
    response = {
        "results": {"closed": True}}

    return response



def close_session_by_credentials(user, session_id, email, password):
    user = User.objects.get(email=email, pk=user.id)

    try:
        session = Session.objects.get(pk=session_id, user=user)

    except Session.DoesNotExist:
        raise InvalidSessionExeption('No session exists')
    
    verified = session.user.check_password(raw_password=password)

    if verified is False:
        raise NoUserExists('Wrong password')
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response


def auth_user(email, password):
    try:
        user = User.objects.get(email=email)
    except:
        raise NoUserExists('Wrong email')
    
    verified = user.check_password(raw_password=password)

    if not verified:
        raise NoUserExists(detail='Invalid password')

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    create_user_session(user=user, refresh_token=refresh_token)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    
    return response


def validate_access_token(access_token):
    decoded = decode_access_token(access_token)

    user = get_user(user_id=decoded['user_id'])
            
    return user


def validate_refresh_token(refresh_token):
    decoded = decode_refresh_token(refresh_token=refresh_token)

    user = get_user(user_id=decoded['user_id'])
            
    return user

        

def validate_register_data(username, password1, password2, email, first_name, last_name):

    if password1 != password2:
        raise serializers.ValidationError({"password": "Password fields didn't match."})

    user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
    user.set_password(password1)
    user.save()


def user_sessions(user):
    return Session.objects.filter(user=user)


def send_code_to_user(user, email):
    try:
        user = User.objects.get(pk=user.id, email=email)
    except User.DoesNotExist:
        raise NoUserExists('Wrong email')

    MAILING_CODE = random.randint(1111,9999)
    
    send_user_message(user, MAILING_CODE)

    user.send_code = MAILING_CODE
    user.time_send = timezone.now()
    user.save()

    response = {
        'sended': True
    }

    return response



def validate_code(user, email, verification_code):

    try:
        user = User.objects.get(email=email, send_code=verification_code, pk=user.id)
    except User.DoesNotExist:
        raise NoUserExists('Invalid data')

    time_send = user.time_send.timestamp() + 120
    current_time = timezone.now().timestamp()

    if current_time > time_send:
        raise serializers.ValidationError('Code expired')

def set_user_password(user, new_password, confirm_password):
    user = get_user(user.id)

    if new_password != confirm_password:
        raise serializers.ValidationError({"password": "Password fields didn't match."})

    user.set_password(new_password)
    user.save()


def set_user_photo(user, photo):

    user = get_user(user_id=user.id)

    user.avatar = photo
    user.save()


def get_user(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user
    except:
        raise NoUserExists

def create_user_session(user, refresh_token):
    user_sessions = Session.objects.filter(user=user).count()

    print(user_sessions)

    if user_sessions >= 3:
        raise InvalidSessionExeption('Please delete one session to continue')
    
    session = Session.objects.create(user=user, refresh_token=refresh_token)
    session.active = True
    session.save()
    return session