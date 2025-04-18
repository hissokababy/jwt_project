import datetime

from project_jwt.celery import app

from mailing_app.services.mailing import MailingService

service = MailingService()

@app.task
def check():

    tasks_lst = service.check_task_date()

    # for task in tasks_lst:
    #     task.receivers.filter()

    print('I be checking your stuff', datetime.datetime.now())





