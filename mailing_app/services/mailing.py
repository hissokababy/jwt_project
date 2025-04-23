import datetime
from django.utils import timezone
from django.db.models import QuerySet
from django.db import transaction
from django.core.mail import send_mass_mail


from jwtapp.models import User

from mailing_app.serializers import TaskSerilizer
from project_jwt.settings import DEFAULT_FROM_EMAIL
from mailing_app.models import Task, TaskReceiver, TaskReport
from mailing_app.exeptions import NoTaskExist, ReceiverIdError, InvalidTaskDate

class MailingService:
    def __init__(self, user: User = None):
        self.user = user

    def get_task(self, pk: int) -> dict:
        try:
            task = Task.objects.prefetch_related('receivers').prefetch_related('reports').get(pk=pk)
        except Task.DoesNotExist:
            raise NoTaskExist
            
        serializer = TaskSerilizer(task)
        return serializer.data

       
    def create_task(self, title: str = None, message: str = None, date: str = None, 
                    receivers: list = None) -> dict:     
        validated_date = self.validate_date(date=date)
        with transaction.atomic():
            task = Task.objects.create(created_by=self.user, title=title,
                                message=message, date=validated_date)
            self.bulk_create_receivers(task=task, receivers=receivers)
            
        serializer = TaskSerilizer(task)
        return serializer.data
    

    def update_task(self, pk: int, defaults: dict) -> dict:
        try:
            task = Task.objects.select_related('updated_by').get(pk=pk)
        except Task.DoesNotExist:
            raise NoTaskExist
        
        if task.completed:
            raise NoTaskExist("you can't change this task it was already completed, create a new task")

        validated_date = self.validate_date(defaults.get('date', task.date))

        task.updated_by = self.user
        task.title = defaults.get('title', task.title)
        task.message = defaults.get('message', task.message)
        task.date = validated_date
        task.save()

        receivers_lst = defaults.get('receivers') # получили список ид пользователей
        receivers_set = set(receivers_lst)

        # ######  проверили на несуществующего пользователя  #####
        users_ids = User.objects.filter(pk__in=receivers_lst).values_list("pk", flat=True)
        users_set = set(users_ids)
        non_existent_users = list(receivers_set - users_set)
        
        if non_existent_users:
            raise ReceiverIdError(f'No users with id: {non_existent_users}')  
        ######  проверили на несуществующего пользователя #####

        ####### удаление получателей #######
        TaskReceiver.objects.exclude(task=task, user__pk__in=receivers_lst).delete()

        ####### добавление новых получателей #######
        all_task_receivers = TaskReceiver.objects.filter(task=task, task__completed=False).values_list('user__pk', flat=True)
        all_task_receivers_set = set(all_task_receivers)

        new_receivers = list(receivers_set - all_task_receivers_set)
        
        if new_receivers:
            self.bulk_create_receivers(task, receivers=new_receivers)
        # ####### добавление новых получателей #######

        serializer = TaskSerilizer(task)
        return serializer.data 

    def bulk_create_receivers(self, task: Task, receivers: list) -> None:
        users = User.objects.filter(pk__in=receivers)
        non_existent_users = list(set(receivers) - set(users.values_list('pk', flat=True)))

        if non_existent_users:
            raise ReceiverIdError(f'No users with id: {non_existent_users}')  
        
        new_receivers = [TaskReceiver(user=user, task=task) for user in users]

        receivers = TaskReceiver.objects.bulk_create(new_receivers)

    def delete_task(self, pk: int) -> None:
        try:
            Task.objects.get(pk=pk).delete()
        except Task.DoesNotExist:
            raise NoTaskExist

    def check_task_date(self) -> QuerySet:
        now = datetime.datetime.now()
        tasks = Task.objects.filter(completed=False, date__lte=now).prefetch_related('receivers')

        for task in tasks:
            task_receivers = task.receivers.values_list('user__email', flat=True)

            if task_receivers:
                try:
                    message = (task.title,
                               task.message,
                               DEFAULT_FROM_EMAIL,
                                task_receivers,
                            )

                    send_mass_mail((message,), fail_silently=False)
                
                    TaskReport.objects.create(task=task, task_compeleted=True,
                                                    total_receivers=len(task_receivers),
                                                    successful=len(task_receivers))
                    task.completed = True
                    task.save()

                except Exception as e:
                    print(e)
                    TaskReport.objects.create(task=task, task_compeleted=False,
                                                    total_receivers=len(task_receivers),
                                                    successful=len(task_receivers), error_detail=str(e))

        return tasks
    
    def validate_date(self, date: datetime):        
        if date < timezone.now() + datetime.timedelta(minutes=5):
            raise InvalidTaskDate("Date should be atleast 5 minutes ahead of the current time!")

        return date
        

