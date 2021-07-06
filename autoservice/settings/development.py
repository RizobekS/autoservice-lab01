# Python imports
from os.path import join

# project imports
from .common import *

DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Email sending
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = join(PROJECT_ROOT, 'emails')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
}
