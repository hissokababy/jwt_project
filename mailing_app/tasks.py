from project_jwt.celery import app

from mailing_app.services.mailing import MailingService


@app.task
def check() -> None:
    service = MailingService()
    service.check_task_date()

