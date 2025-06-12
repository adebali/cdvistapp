
import os
from flask import Flask
from celery import Celery


def make_celery(app):
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_url = f'redis://{redis_host}:6379/0'

    celery = Celery(
        app.import_name,
        backend=redis_url,
        broker=redis_url
    )
    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app'])
    return celery

app = Flask(__name__)
celery = make_celery(app)
