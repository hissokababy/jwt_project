from rest_framework.exceptions import APIException
from rest_framework import status

class DoesExsistUser(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('A server error occurred.')
    default_code = 'error'

class InActiveSession(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Inactive session.')
    default_code = 'error'