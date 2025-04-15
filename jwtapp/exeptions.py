from rest_framework.exceptions import APIException
from rest_framework import status


class NoUserExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('User does not exist.')
    default_code = 'error'

class InvalidSessionExeption(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('Invalid session.')
    default_code = 'invalid'


class InvalidTokenExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive session.')
    default_code = 'error'

class InvalidCodeExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Invalid verification code.')
    default_code = 'error'

