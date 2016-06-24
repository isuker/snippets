#!/usr/bin/python
#coding:utf-8
import requests
from celery import Celery, platforms
from flask import Flask
utf8 = lambda u: u.encode('utf-8')


app = Flask(__name__)

def make_celery(app):
    celery = Celery(app.__class__)
    platforms.C_FORCE_ROOT = True
    celery.config_from_object('setting')
    #celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return (app,celery)

app, celery = make_celery(app)

@celery.task(name="tasks.sns_share")
def sns_share(words):
    print "sns_share start to say %s" %words
    return words

if __name__ == '__main__':
    with app.app_context():
        celery.start()
