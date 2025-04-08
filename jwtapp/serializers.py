from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User

from jwtapp.services.sessions import create_user, validate_closing_session
from jwtapp.tokens import check_session_activity, validate_token
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
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = create_user(validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    email = serializers.EmailField()
    device_type = serializers.CharField(required=True)
    password = serializers.CharField(required=True, validators=[validate_password])

    


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            validate_token(value)
            check_session_activity(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value
    

class PasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField()
    email = serializers.EmailField()
    send_code = serializers.BooleanField()

    def validate_phone(self, value):
        return value

    def validate_phone(self, value):
        return value

# Работа с сессиями

class MySessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('id', 'device_type', 'created_at', 'updated_at')


class CloseSessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()

    def validate_session_id(self, value):
        try:
            validate_closing_session(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value


class CloseAllSessionsSerializer(serializers.Serializer):
    current_session_id = serializers.IntegerField()

    def validate_session_id(self, value):
        try:
            validate_closing_session(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value



class CloseSessionByCredentialsSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_session_id(self, value):
        try:
            validate_closing_session(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value
    
    def validate_password(self, value):
        return value