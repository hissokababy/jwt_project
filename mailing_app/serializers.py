from rest_framework import serializers


class CreateTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()
    date = serializers.DateTimeField()
    receivers = serializers.ListField(
        child = serializers.IntegerField()
    )


class TaskReceiverSerializer(serializers.Serializer):
    user = serializers.IntegerField()


class TaskReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task_compeleted = serializers.BooleanField()
    total_receivers = serializers.IntegerField()
    successful = serializers.IntegerField()
    unsuccessful = serializers.IntegerField()
    

class TaskSerilizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    message = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    receivers = TaskReceiverSerializer(many=True)
    reports = TaskReportSerializer(many=True)
