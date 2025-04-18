import datetime
from django.db.models import QuerySet
from django.core.mail import send_mail

from jwtapp.models import User

from mailing_app.models import Task, TaskReceiver, TaskReport
from mailing_app.exeptions import NoTaskExist
from project_jwt.settings import DEFAULT_FROM_EMAIL

class MailingService:
    def __init__(self):
        pass

    def create_task(self, user: User, title: str, message: str, date: str, receivers: list) -> None:

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

        other_receivers = TaskReceiver.objects.filter(task=task, is_active=True).exclude(user__pk__in=receivers_lst)

        inactive_lst = []

        for receiver in other_receivers:
            receiver.is_active = False
            inactive_lst.append(receiver)

        TaskReceiver.objects.bulk_update(inactive_lst, fields=['is_active'])

        active_receivers = [i.user.pk for i in TaskReceiver.objects.filter(task=task, is_active=True)]
        new_receivers = []

        for receiver in receivers_lst:
            if receiver not in active_receivers:
                new_receivers.append(receiver)
        
        self.bulk_create_receivers(task=task, receivers=new_receivers)

        return task    


    def bulk_create_receivers(self, task: Task, receivers: list) -> None:
        users = User.objects.filter(pk__in=receivers)
        lst = []

        for user in users:
            lst.append(TaskReceiver(user=user, task=task))
        
        receivers = TaskReceiver.objects.bulk_create(lst)


    def delete_task(self, pk: int) -> None:
        try:
            task = Task.objects.get(pk=pk).delete()
        except Task.DoesNotExist:
            raise NoTaskExist

    def check_task_date(self) -> TaskReport:
        tasks = Task.objects.filter(completed=False, date__lte=datetime.datetime.now())

        successful = 0
        unsuccessful = 0

        if tasks.exists():

            for task in tasks:
                task_receivers = task.receivers.filter(is_active=True)

                for receiver in task_receivers:
                    try:
                        send_mail(
                        subject=task.title,
                        message=task.message,
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[receiver.user.email],
                        fail_silently=False,
                        )
                        successful += 1
                    except:
                        unsuccessful += 1

                report = TaskReport.objects.create(task=task, task_compeleted=True,
                                                total_receivers=task_receivers.count(),
                                                successful=successful, unsuccessful=unsuccessful)

                task.completed = True
                task.save()

            return report
    
