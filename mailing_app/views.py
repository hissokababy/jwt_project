from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from mailing_app.serializers import CreateTaskSerializer, TaskSerilizer
from mailing_app.services.mailing import MailingService
from mailing_app.tasks import check


# Create your views here.

@extend_schema(tags=["Mailing"])
class TaskDetailView(APIView):
    permission_classes = [IsAdminUser]
    service = MailingService()


    @extend_schema(responses=CreateTaskSerializer)    
    def post(self, request, pk=None, format=None):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        self.service.create_task(request.user, *data.values())

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=TaskSerilizer)
    def get(self, request, pk=None, format=None):
        task = self.service.get_task_by_id(pk)

        serializer = TaskSerilizer(data=task)
        serializer.is_valid(raise_exception=True)

        self.service.check_task_date()

        return Response(serializer.validated_data)
    
    @extend_schema(responses=TaskSerilizer)
    def put(self, request, pk=None, format=None):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.service.update_task(pk, user=request.user, defaults=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
    

    def delete(self, request, pk=None, format=None):
        self.service.delete_task(pk)
        return Response(status=status.HTTP_200_OK)
