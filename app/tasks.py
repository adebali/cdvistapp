# import time
# from . import celery


#!/usr/bin/env python

import os
import time
from celery import Celery, current_task


env=os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL','redis://localhost:6379'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND','redis://localhost:6379')

import sys
sys.path.append('/cdvist/app/lib')
import cdvist_pipeline

celery= Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


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


@celery.task(name='tasks.add')
def add(x, y):
    current_task.update_state(state='PROGRESS', meta={'current': 1, 'total': x+y})
    time.sleep(5) # lets sleep for a while before doing the gigantic addition task!
    return x + y

@celery.task(name='tasks.out')
def out(jobId):
    current_task.update_state(state='PROGRESS', meta={'jobId': jobId})
    # cdvist_pipeline.main(inputJson)
    time.sleep(5)
    return jobId

@celery.task(name='tasks.pipeline')
def pipeline(requestJson):
    cdvist_pipeline.runPipeline(requestJson, True)


# @celery.task(name='aqueriumTask.query')
# def runSunQuery(argJsonFileName):
#     sunQuery.main(argJsonFileName)

# @celery.task(name='aqueriumTask.customInput')
# def runBlastXml2nodedJson(argJsonFileName):
#     blastXml2nodedJson.main(argJsonFileName)
