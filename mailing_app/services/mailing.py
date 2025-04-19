import datetime
from django.db.models import QuerySet
from django.db import transaction


from jwtapp.models import User

from mailing_app.models import Task, TaskReceiver
from mailing_app.exeptions import NoTaskExist, ReceiverIdError

class MailingService:
    def __init__(self):
        pass

    def create_task(self, user: User, title: str, message: str, date: str, receivers: list) -> None:
        with transaction.atomic():
            _, task = Task.objects.get_or_create(created_by=user, title=title,
                                    message=message, date=date)

            if not task:
                raise NoTaskExist('Task already exists')

            task = Task.objects.get(created_by=user, title=title,
                                    message=message, date=date)
            
            self.bulk_create_receivers(task=task, receivers=receivers)


    def get_task_by_id(self, pk: int) -> dict:
        try:
            task = Task.objects.get(pk=pk)
            receivers = task.receivers.all()
            reports = task.reports.all()

        except Task.DoesNotExist:
            raise NoTaskExist

        receivers_data = [{'user': i.user.pk} for i in receivers]
        reports_data = [
            {  
                'id': i.pk, 
                'task_compeleted': i.task_compeleted,
                'total_receivers': i.total_receivers,
                'successful': i.successful,
                'unsuccessful': i.unsuccessful,
            } 
            
            for i in reports]

        task_data = {
            'id': task.pk,
            'title': task.title,
            'message': task.message,
            'date': task.date,
            'receivers': receivers_data,
            'reports': reports_data,
        }

        return task_data


    def update_task(self, pk: int, user: User, defaults: dict) -> Task:
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NoTaskExist

        task.updated_by = user.pk
        task.title = defaults.get('title')
        task.message = defaults.get('message')
        task.date = defaults.get('date')
        task.save()

        receivers_lst = defaults.get('receivers')
        users = User.objects.filter(pk__in=receivers_lst)
        user_ids = [i.pk for i in users]

        for i in receivers_lst:
            if i not in user_ids:
                raise ReceiverIdError(f'No user with id {i}')
            
        active_receivers = TaskReceiver.objects.filter(task=task, is_active=True)

        print(receivers_lst)
        print(active_receivers)
        
        deactive_receivers = TaskReceiver.objects.exclude(user__pk__in=receivers_lst)
        deactive_lst = []

        for i in deactive_receivers:
            i.is_active = False
            deactive_lst.append(i)
        
        TaskReceiver.objects.bulk_update(deactive_lst, fields=['is_active'])

        return task    


    def bulk_create_receivers(self, task: Task, receivers: list) -> None:
        users = User.objects.filter(pk__in=receivers)
        user_ids = [i.pk for i in users]
        lst = []

        for user in users:
            lst.append(TaskReceiver(user=user, task=task))

        for i in receivers:
            if i not in user_ids:
                raise ReceiverIdError(f'No user with id {i}')
        
        receivers = TaskReceiver.objects.bulk_create(lst)


    def delete_task(self, pk: int) -> None:
        try:
            task = Task.objects.get(pk=pk).delete()
        except Task.DoesNotExist:
            raise NoTaskExist

    def check_task_date(self) -> QuerySet:
        tasks = Task.objects.filter(completed=False, date__lte=datetime.datetime.now())

        return tasks
    
