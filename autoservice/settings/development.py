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
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'autoservice_development',
        'USER': 'dabud',
        'PASSWORD': '8ghgVa7k_5Y7LK*',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    },
}

LOGGING = {
    'version': 1,
    'filters': {
        'slow_sql': {'()': 'autoservice.logging.filters.SlowSQLQueryFilter'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}
    },
    'handlers': {
        'sql_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_ROOT, 'run', 'logs', 'sql_queries.log')
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_ROOT, 'run', 'logs', 'django.log')
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['sql_file'],
            'filters': ['require_debug_true'],
        }
    }
}
