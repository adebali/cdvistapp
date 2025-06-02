from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult
from .tasks import add_together  # import tasks here
from .tasks import long_task  # import tasks here



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

@app.route('/')
def index():
    return '<a href="/start-task">Start Task</a>'

@app.route('/start-task')
def start_task():
    task = long_task.apply_async(args=[10])
    status_url = f'/task-status/{task.id}'
    return f'Task started! <a href="{status_url}">Check status here</a>', 202

@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Waiting in queue...'}
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'percent': int((task.info.get('current', 0) / task.info.get('total', 1)) * 100)
        }
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}

    return jsonify(response)

@app.route('/run-task')
def run_task():
    result = add_together.delay(10, 20)
    return f'Task launched! Task ID: {result.id}'

@app.route('/task-result/<task_id>')
def task_result(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        return f"Result: {result.result}"
    else:
        return "Task is still running. Please check back later."