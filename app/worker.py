#!/usr/bin/env python

import os
from celery import Celery

env=os.environ
CELERY_BROKER_URL=env.get('REDIS_HOST','redis://redis:6379'),
CELERY_RESULT_BACKEND=env.get('REDIS_HOST','redis://redis:6379')

celery= Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)
