
from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://redis:6379/0',
        broker='redis://redis:6379/0'
    )
    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app'])
    return celery

app = Flask(__name__)
celery = make_celery(app)

# from .tasks import add_together  # import tasks here

# @app.route('/')
# def index():
#     return 'Hello from Flask! Go to /run-task to launch a background job.'

# @app.route('/run-task')
# def run_task():
#     result = add_together.delay(10, 20)
#     return f'Task launched! Task ID: {result.id}'
