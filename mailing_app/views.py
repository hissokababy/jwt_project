from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from jwtapp.authentication import JWTAuthentication
from mailing_app.serializers import CreateTaskSerializer, TaskSerilizer
from mailing_app.services.mailing import MailingService

# Create your views here.

@extend_schema(tags=["Mailing"])
class TaskDetailView(APIView):
    permission_classes = [IsAdminUser]
    # authentication_classes = [JWTAuthentication]
    serializer_class = CreateTaskSerializer
    service = MailingService


    @extend_schema(responses=CreateTaskSerializer)    
    def post(self, request, pk=None, format=None):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        task = self.service().create_task(title=data.get('title'), message=data.get('message'),
                                 date=data.get('date'), receivers=data.get('receivers'))

        return Response(task, status=status.HTTP_201_CREATED)

    @extend_schema(responses=TaskSerilizer)
    def get(self, request, pk=None, format=None):

        task = self.service().get_task(pk=pk)
        return Response(task, status=status.HTTP_200_OK)

    
    @extend_schema(responses=TaskSerilizer)
    def put(self, request, pk=None, format=None):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.service(user=request.user).update_task(pk=pk, defaults=serializer.validated_data)

        return Response(task, status=status.HTTP_200_OK)
    

    def delete(self, request, pk=None, format=None):
        self.service().delete_task(pk=pk)
        return Response(status=status.HTTP_200_OK)
