import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.conf.task_default_queue = "celery"

app.conf.broker_connection_retry_on_startup = True

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["web"])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
