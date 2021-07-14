# Python imports
from os.path import join

# project imports
from .common import *

DEBUG = True

STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Email sending
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = join(PROJECT_ROOT, 'emails')
EMAIL_HOST_USER = 'no-reply@example.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(r'C:\Users\David\Desktop\temp', 'dev.sqlite3'),
    }
}
