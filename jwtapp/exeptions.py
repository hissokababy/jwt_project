from rest_framework.exceptions import APIException
from rest_framework import status


class NoUserExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('User does not exist.')
    default_code = 'no_user'

class InvalidSessionExeption(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('Invalid session.')
    default_code = 'invalid_session'


class InvalidTokenExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive token.')
    default_code = 'invalid_token'

class InvalidCodeExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Invalid verification code.')
    default_code = 'invalid_code'


class InvalidPasswordExeption(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('Invalid password.')
    default_code = 'invalid_password'