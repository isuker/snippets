import os
# configuration

# root
ROOT = os.path.abspath(os.path.dirname(__file__))

# debug
DEBUG = True

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

CSRF_ENABLED  = True

# database
DB = r'/db/app.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + ROOT + DB
SQLALCHEMY_NATIVE_UNICODE = None

# admin
ADMINS = ['ray.chen@emc.com']
MAIL_ENABLE = True
ADMIN_MAIL = 'ray.chen@emc.com'

CACHE_TYPE = 'simple'


# uploads
UPLOADS_DEFAULT_DEST = ROOT + '/app/static/uploads'

# celery setting
BROKEN_URL="amqp://10.32.191.173"
#CELERY_RESULT_BACKEND="amqp"
CELERY_RESULT_BACKEND="db+sqlite:///db/job-results.sqlite"
CELERY_IGNORE_RESULT = False
CELERY_TASK_RESULT_EXPIRES=None
