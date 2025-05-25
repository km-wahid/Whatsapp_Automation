from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
# from celery.contrib import rdb

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Whatsapp.settings')

app = Celery('Whatsapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()




@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# from celery import Celery

# app = Celery(
#     "Whatsapp",
#     broker="sqla+postgresql://postgres:almighty@localhost:5432/WhatsApp_copy2",
#     backend="db+postgresql://postgres:almighty@localhost:5432/WhatsApp_copy2"
    


# )

# app.conf.update(
#     result_extended=True  # This helps with task tracking
# )


#   macOS  issues
app.conf.worker_pool = 'solo'
broker_connection_retry = True  # still used during normal operation
broker_connection_retry_on_startup = True  # new requirement for startup retry