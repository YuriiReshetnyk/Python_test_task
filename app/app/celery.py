"""
Celery configuration.
"""
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = [
    Queue('random_data_api',
          Exchange('random_data_api'),
          routing_key='random_data_api')
]

app.conf.task_routes = {
    'celery_tasks.tasks.task_fetch_user.task_fetch_user_data':
        {'queue': 'random_data_api'},
    'celery_tasks.tasks.task_fetch_credit_card.task_fetch_credit_card_data':
        {'queue': 'random_data_api'},
    'celery_tasks.tasks.task_fetch_address.task_fetch_address_data':
        {'queue': 'random_data_api'},
}

app.conf.beat_schedule = {
    'fetch_user_data': {
        'task': 'celery_tasks.tasks.task_fetch_user.'
                'task_fetch_user_data',
        'schedule': crontab(hour='*', minute='*')
    },
    'fetch_credit_card_data': {
        'task': 'celery_tasks.tasks.task_fetch_credit_card.'
                'task_fetch_credit_card_data',
        'schedule': crontab(hour='*', minute='*')
    },
    'fetch_address_data': {
        'task': 'celery_tasks.tasks.task_fetch_address.'
                'task_fetch_address_data',
        'schedule': crontab(hour='*', minute='*')
    },
}

app.conf.broker_connection_retry_on_startup = True
app.conf.worker_prefetch_multiplier = 1

app.autodiscover_tasks(['celery_tasks.tasks.task_fetch_address',
                        'celery_tasks.tasks.task_fetch_credit_card',
                        'celery_tasks.tasks.task_fetch_user'])
