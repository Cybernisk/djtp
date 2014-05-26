# coding: utf-8
from app.settings.dist import *
try:
    from app.settings.local import *
except ImportError:
    pass
from app.settings.messages import *
from app.settings.dist import INSTALLED_APPS

DEBUG = True
DEV_SERVER = True
USER_FILES_LIMIT = 1.2 * 1024 * 1024
SEND_MESSAGES = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '_test.sqlite',
    }, 
}
INSTALLED_APPS = list(INSTALLED_APPS)
removable = ['south', ]
for app in removable:
    if app in INSTALLED_APPS:
        INSTALLED_APPS.remove(app)

TEST_DATABASE_NAME = DATABASES['default']['NAME'] if \
    DATABASES['default']['NAME'].startswith('test_') else \
    'test_' + DATABASES['default']['NAME']
