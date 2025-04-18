from rest_framework.exceptions import APIException
from rest_framework import status


class NoTaskExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Task does not exist.')
    default_code = 'no_task'