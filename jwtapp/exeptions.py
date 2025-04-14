from rest_framework.exceptions import APIException
from rest_framework import status

class NoUserExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('User does not exist.')
    default_code = 'error'

class InvalidSessionExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive session.')
    default_code = 'error'

class InvalidTokenExeption(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive session.')
    default_code = 'error'

