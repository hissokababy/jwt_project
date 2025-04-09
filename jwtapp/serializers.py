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
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    email = serializers.EmailField()
    device_type = serializers.CharField()
    password = serializers.CharField(required=True, validators=[validate_password])



class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    

class PasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField()
    email = serializers.EmailField()
    send_code = serializers.BooleanField()


# Работа с сессиями

class MySessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('id', 'device_type', 'created_at', 'updated_at', 'active','user')


class CloseSessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()


class CloseAllSessionsSerializer(serializers.Serializer):
    current_session_id = serializers.IntegerField()



class CloseSessionByCredentialsSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=True)
    phone = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(required=True, validators=[validate_password])

