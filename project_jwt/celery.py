import os

from celery import Celery

from project_jwt.settings import CELERY_WORKER_TIME_INTERVAL

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_jwt.settings')

app = Celery(
    'mailing_app',
)


app.conf.beat_schedule = {
 'check': {
     'task': 'mailing_app.tasks.check',
     'schedule': CELERY_WORKER_TIME_INTERVAL
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


