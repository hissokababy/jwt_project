from rest_framework.exceptions import APIException
from rest_framework import status


class NoTaskExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Task does not exist.')
    default_code = 'no_task'


class ReceiverIdError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('User does not exist.')
    default_code = 'no_user'

class InvalidTaskDate(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('invalid task date.')
    default_code = 'invalid_date'