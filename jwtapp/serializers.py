from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from jwtapp.models import User
from jwtapp.models import Session

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True, validators=[validate_password])


class ResponseLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResponsePasswordResetSerializer(serializers.Serializer):
    send_code = serializers.BooleanField(default=True)


class CheckVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])



# Работа с сессиями

class MySessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('id', 'device_type', 'created_at', 'updated_at', 'active','user')


class CloseSessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()

class ResponseCloseSessionSerializer(serializers.Serializer):
    closed = serializers.BooleanField(default=True)


class CloseAllSessionsSerializer(serializers.Serializer):
    current_session_id = serializers.IntegerField()



class CloseSessionByCredentialsSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=True)
    email = serializers.EmailField()
    password = serializers.CharField(required=True, validators=[validate_password])


class ChangeProfilePhotoSerializer(serializers.Serializer):
    photo = serializers.FileField()
