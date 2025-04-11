import random
import jwt
from jwtapp.models import Session
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import status
from django.utils import timezone

class DoesExsistUser(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('A server error occurred.')
    default_code = 'error'

class InActiveSession(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive session.')
    default_code = 'error'

from jwtapp.tokens import decode_access_token, decode_refresh_token, generate_access_token, generate_refresh_token

from jwt import exceptions
from rest_framework import serializers

from jwtapp.models import Session, User



def generate_user_tokens(token):

    try:    
        session = Session.objects.get(refresh_token=token)

        if session.user.is_active and session.active:

            access_token = generate_access_token(session.user)
            refresh_token = generate_refresh_token(session.user)

            response = {
                'access': access_token,
                'refresh': refresh_token
            }

            session.refresh_token = refresh_token
            session.save()
        
            return response
        
        else:
            raise serializers.ValidationError('Inactive session')
    
    except Session.DoesNotExist:
        raise serializers.ValidationError('Session not found')

    except Exception as e:
        raise serializers.ValidationError(e)


def close_session(session_id=None, refresh_token=None):
    try:
        if session_id:
            session = Session.objects.get(pk=session_id)
        elif refresh_token:
            session = Session.objects.get(refresh_token=refresh_token)

        session.active = False
        session.save()

        response = {
        "results": {"closed": True}}
        return response
    
    except Session.DoesNotExist:
        raise serializers.ValidationError('Session does not exist')


def close_sessions(current_session_id):
    try:
        current_session = Session.objects.get(pk=current_session_id)
    except Session.DoesNotExist:
        raise DoesExsistUser

    if not current_session.active:
        raise InActiveSession
    
    user_sessions = Session.objects.filter(user=current_session.user, active=True).exclude(pk=current_session.id)

    sessions = []

    for session in user_sessions:
        session.active = False
        sessions.append(session)

    updated = Session.objects.bulk_update(sessions, fields=['active'])
    
    response = {
        "results": {"close;';d": True}}

    return response



def close_session_by_credentials(session_id, email, password):
    
    try:
        session = Session.objects.get(pk=session_id)
        user = User.objects.get(email=email)

    except Session.DoesNotExist or User.DoesNotExist:
        raise serializers.ValidationError('Matching query does not exist')
    
    
    verified = session.user.check_password(raw_password=password)

    if verified is False:
        return None
    
    session.active = False
    session.save()

    response = {
        "results": {"closed": True}}
    
    return response


def auth_user(email, device_type, password):

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
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        user_session = Session.objects.create(user=user, refresh_token=refresh_token)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    return response


def verify_phone_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        raise serializers.ValidationError('No such user')


def validate_token(access_token=None, refresh_token=None):
    try:
        if access_token:
            decoded = decode_access_token(access_token)

            user_id = decoded['user_id']

            user = User.objects.get(id=user_id)
            
            return user

        elif refresh_token:

            decoded = decode_refresh_token(refresh_token=refresh_token)

            user_id = decoded['user_id']

            user = User.objects.get(id=user_id)
            
            return refresh_token

    except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

    except exceptions.DecodeError:
        raise AuthenticationFailed('Token expired')

    except exceptions.ExpiredSignatureError:
        raise AuthenticationFailed(exceptions.ExpiredSignatureError.__name__)
        

def validate_register_data(validated_data):

    if validated_data['password'] != validated_data['password2']:
        raise serializers.ValidationError({"password": "Password fields didn't match."})

    user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
    user.set_password(validated_data['password'])
    user.save()

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_session = Session.objects.create(user=user, refresh_token=refresh_token)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return response


def validate_refresh_token(refresh_token):

    try:
        refresh_token = validate_token(refresh_token=refresh_token)

    except Exception as e:
        raise serializers.ValidationError(e)
    
    return refresh_token 


def user_sessions(user):
    return Session.objects.filter(user=user)


def validate_session_id(session_id):
    try:
        session = Session.objects.get(pk=session_id)
        return session
    except Session.DoesNotExist:
        return False


def send_code_to_user(user):
    MAILING_CODE = random.randint(1111,9999)
    
    send_code_to_user(user, MAILING_CODE)

    user.send_code = MAILING_CODE
    user.time_send = timezone.now()
    user.save()

    response = {
        'sended': True
    }

    return response



def validate_code(email, device_type, verification_code):
    try:
        user = User.objects.get(email=email, send_code=verification_code)
    except User.DoesNotExist:
        raise serializers.ValidationError('No such user')

    time_send = user.time_send.timestamp() + 120
    current_time = timezone.now().timestamp()

    if current_time > time_send:
        raise serializers.ValidationError('Code expired send new')

    
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_session = Session.objects.create(user=user, refresh_token=refresh_token)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return response