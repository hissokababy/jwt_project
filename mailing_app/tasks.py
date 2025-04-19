from project_jwt.celery import app
from django.core.mail import send_mail

from mailing_app.services.mailing import MailingService
from project_jwt.settings import DEFAULT_FROM_EMAIL
from mailing_app.models import TaskReport

service = MailingService()

@app.task
def check() -> None:

    tasks = service.check_task_date()

    if tasks.exists():

        for task in tasks:
            task_receivers = task.receivers.filter(is_active=True)

            for receiver in task_receivers:
                send_mail(
                subject=task.title,
                message=task.message,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[receiver.user.email],
                fail_silently=False,
                )

            report = TaskReport.objects.create(task=task, task_compeleted=True,
                                                total_receivers=task_receivers.count(),
                                                successful=task_receivers.count())

            task.completed = True
            task.save()

            task.receivers.filter(is_active=False).delete()

    else:
        print('no tasks to send')







