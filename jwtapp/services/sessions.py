import random

from django.db.models import QuerySet
from django.utils import timezone

from jwtapp.utils import send_user_message
from jwtapp.tokens import decode_access_token, decode_refresh_token, generate_access_token, generate_refresh_token
from jwtapp.models import Session, User
from jwtapp.exeptions import InvalidCodeExeption, InvalidPasswordExeption, NoUserExists, InvalidSessionExeption


def generate_user_tokens(token: str) -> dict:
    decoded = decode_refresh_token(token)
    
    user = get_user(decoded['user_id'])

    try:
        session = Session.objects.get(user=user, refresh_token=token, active=True)
    except Session.DoesNotExist:
        raise InvalidSessionExeption

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    session.refresh_token = refresh_token
    session.save()

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return response


def close_session_by_id(user: User, session_id: int) -> dict:
    user = get_user(user.id)

    try:
        session = Session.objects.get(pk=session_id, user=user, active=True)
    except Session.DoesNotExist:
        raise InvalidSessionExeption('Session does not exist')
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response

def close_session_by_token(user: User, refresh_token: str) -> dict:
    user = get_user(user.id)

    try:
        session = Session.objects.get(refresh_token=refresh_token, user=user, active=True)
    except Session.DoesNotExist:
        raise InvalidSessionExeption('Session does not exist')
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response
    

def close_sessions(user: User, current_session_id: int) -> dict:
    user = get_user(user.id)

    try:
        current_session = Session.objects.get(pk=current_session_id, user=user, active=True)
    except Session.DoesNotExist:
        raise InvalidSessionExeption('Session does not exist')

    if not current_session.active:
        raise InvalidSessionExeption
    
    user_sessions = Session.objects.filter(user=user, active=True).exclude(pk=current_session.id)

    sessions = []

    for session in user_sessions:
        session.active = False
        sessions.append(session)

    Session.objects.bulk_update(sessions, fields=['active'])
    
    response = {
        "results": {"closed": True}}

    return response



def close_session_by_credentials(session_id: int, email: str, password: str) -> dict:
    user = User.objects.get(email=email)
    verified = user.check_password(raw_password=password)

    if verified is False:
        raise NoUserExists('Wrong password')
    if not user.is_active:
        raise NoUserExists

    try:
        session = Session.objects.get(pk=session_id, user=user, active=True)

    except Session.DoesNotExist:
        raise InvalidSessionExeption('No session exists')

    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response


def auth_user(email: str, password: str) -> dict:
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            raise NoUserExists
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


def validate_access_token(access_token: str) -> User:
    decoded = decode_access_token(access_token)

    user = get_user(user_id=decoded['user_id'])
            
    return user


def validate_refresh_token(refresh_token: str) -> User:
    decoded = decode_refresh_token(refresh_token=refresh_token)

    user = get_user(user_id=decoded['user_id'])
            
    return user

        

def validate_register_data(username: str, password: str, email: str, first_name: str, last_name: str) -> None:

    user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
    user.set_password(password)
    user.save()


def user_sessions(user: User) -> QuerySet[Session]:
    return Session.objects.filter(user=user, active=True)


def send_code_to_user(user: User, email: str) -> dict:
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


def validate_code(user: User, email: str, verification_code: str, new_password: str) -> None:
    try:
        user = User.objects.get(email=email, send_code=verification_code, pk=user.id)
        if not user.is_active:
            raise NoUserExists('Invalid data')
        
    except User.DoesNotExist:
        raise NoUserExists('Invalid data')

    time_send = user.time_send.timestamp() + 120
    current_time = timezone.now().timestamp()

    if current_time > time_send:
        raise InvalidCodeExeption
    
    old_password = user.check_password(new_password)
    if old_password:
        raise InvalidPasswordExeption("This password was already used as old, enter a different password!")

    user.set_password(new_password)
    user.save()


def set_user_photo(user: User, photo: str) -> None:

    user = get_user(user_id=user.id)

    user.avatar = photo
    user.save()


def get_user(user_id: int) -> User:
    try:
        user = User.objects.get(pk=user_id)
        if user.is_active:
            return user
    except:
        raise NoUserExists


def create_user_session(user: User, refresh_token: str) -> Session:
    user_sessions = Session.objects.filter(user=user, active=True).count()

    if user_sessions >= 3:
        raise InvalidSessionExeption('Please delete one session to continue')
    
    session = Session.objects.create(user=user, refresh_token=refresh_token, active=True)
    session.active = True
    session.save()
    return session