import jwt
from jwtapp.models import Session
from rest_framework.exceptions import AuthenticationFailed

from project_jwt.settings import ALGORITHMS, ACCESS_TOKEN_SECRET_KEY, REFRESH_TOKEN_SECRET_KEY
from jwtapp.tokens import decode_access_token, decode_refresh_token, generate_access_token, generate_refresh_token

from jwt import exceptions
from rest_framework import serializers

from jwtapp.models import Session, User


def create_user_session(user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_session = Session.objects.create(user=user, refresh_token=refresh_token)

    response = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response


def get_user(user_id):
    user = User.objects.filter(id=user_id).first()

    if user:
        return user


def generate_user_tokens(token):

    try:    
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

    user_sessions = [i for i in Session.objects.get(pk=current_session_id).user.sessions.all()]

    for session in user_sessions:
        if session.pk != current_session_id:
            session.active = False
        
        session.save()
    
    response = {
        "results": {"closed": True}}

    return response



def close_session_by_credentials(session_id, phone, email, password):
    
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


def auth_user(phone, email, device_type, password):

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


def check_code_time(current_time):
    ...




def update_token(user_ip, user, token):
    try:
        session = Session.objects.get(user=user, user_ip=user_ip)
    except Session.DoesNotExist:
        raise serializers.ValidationError('Session DoesNotExist')

    if not token == session.refresh_token:
        raise AuthenticationFailed('invalid token')

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    session.refresh_token = refresh_token
    session.save()

    response = {
        'access': access_token,
        'refresh': refresh_token
    }

    return response


def create_jwt(request, user_ip, user):
    header = request.headers.get("Authorization")

    parts = header.split()
    if len(parts) == 0:
        return None
    
    jwt_token = update_token(user_ip, user, header)
    return jwt_token


def validate_token(access_token=None, refresh_token=None):
    try:
        if access_token:
            decoded = decode_access_token(access_token)

            user_id = decoded['user_id']

            user = User.objects.get(id=user_id)
            
            return user

        elif refresh_token:
            decoded = decode_refresh_token(refresh_token)

            user_id = decoded['user_id']

            user = User.objects.get(id=user_id)
            
            return refresh_token

    except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

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

    response = create_user_session(user=user)

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
