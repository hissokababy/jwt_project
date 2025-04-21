import datetime
from django.db.models import QuerySet
from django.db import transaction
from django.core.mail import send_mail
from django.forms.models import model_to_dict


from jwtapp.models import User

from project_jwt.settings import DEFAULT_FROM_EMAIL
from mailing_app.models import Task, TaskReceiver, TaskReport
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
            task = Task.objects.prefetch_related('receivers').prefetch_related('reports').get(pk=pk)
        except Task.DoesNotExist:
            raise NoTaskExist
        
        data = model_to_dict(task)
        reports_lst = [model_to_dict(i) for i in task.reports.all()]

        data.update({'receivers': list(task.receivers.values_list('user__pk', flat=True))})
        data.update({'reports': reports_lst})
        
        return data


    def update_task(self, pk: int, user: User, defaults: dict) -> Task:
        try:
            task = Task.objects.select_related('updated_by').get(pk=pk)
        except Task.DoesNotExist:
            raise NoTaskExist

        task.updated_by = user
        task.title = defaults.get('title', task.title)
        task.message = defaults.get('message', task.message)
        task.date = defaults.get('date', task.date)
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

        # ####### добавление новых получателей #######
        all_task_receivers = TaskReceiver.objects.filter(task=task, task__completed=False).values_list('user__pk', flat=True)
        all_task_receivers_set = set(all_task_receivers)

        new_receivers = list(receivers_set - all_task_receivers_set)
        
        if new_receivers:
            self.bulk_create_receivers(task, receivers=new_receivers)
        # ####### добавление новых получателей #######

        return task    


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
        tasks = Task.objects.filter(completed=False, date__lte=datetime.datetime.now()).prefetch_related('receivers__user__email')
        
        if tasks.exists():
            successful = 0

            for task in tasks:
                task_receivers = task.receivers.all()

                if task_receivers.exists():
                    for task_receiver in task_receivers:
                        if task_receiver.user.email:
                            send_mail(
                                subject=task.title,
                                message=task.message,
                                from_email=DEFAULT_FROM_EMAIL,
                                recipient_list=[task_receiver.user.email],
                                fail_silently=False,
                            )
                            
                            successful += 1

                    TaskReport.objects.create(task=task, task_compeleted=True,
                                                        total_receivers=task_receivers.count(),
                                                        successful=successful)
                    task.completed = True
                    task.save()

        else:
            print('no tasks to send')

        return tasks
    


# tasks = Task.objects.select_related("created_by").prefetch_related("receivers__created_by").filter() # 10

# for task in tasks:
#     task.created_by
#     task.created_by_id
#     receivers = task.receivers.all() # 2
#     for receiver in receivers:
#         receiver.created_by


