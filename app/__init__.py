
# from flask import Flask
# from celery import Celery

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend='redis://redis:6379/0',
#         broker='redis://redis:6379/0'
#     )
#     celery.conf.update(app.config)
#     celery.autodiscover_tasks(['app'])
#     return celery

# app = Flask(__name__)
# celery = make_celery(app)
