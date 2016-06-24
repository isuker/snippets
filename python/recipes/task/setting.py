import os
# configuration

# debug
DEBUG = True

# celery setting
BROKEN_URL="amqp://localhost"
#CELERY_RESULT_BACKEND="amqp"
CELERY_RESULT_BACKEND="db+sqlite:///job-results.sqlite"
CELERY_IGNORE_RESULT = False
CELERY_TASK_RESULT_EXPIRES=None
