import time
from . import celery

@celery.task
def add_together(a, b):
    time.sleep(30)
    return a + b


@celery.task(bind=True)
def long_task(self, total_steps):
    for i in range(total_steps):
        time.sleep(1)  # simulate work
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': total_steps})
    return {'current': total_steps, 'total': total_steps, 'status': 'Task completed!'}
