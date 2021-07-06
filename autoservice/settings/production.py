from os import environ

from .common import *

print(ROOT_URLCONF)

# turn off all debugging
DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': str(environ.get("DB_NAME")),
        'USER': str(environ.get("DB_USER")),
        'PASSWORD': str(environ.get("DB_PASSWORD")),
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

# Email sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = str(environ.get("EMAIL_HOST"))
EMAIL_PORT = 587
EMAIL_HOST_USER = str(environ.get("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(environ.get("EMAIL_HOST_PASSWORD"))
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ##### SECURITY CONFIGURATION ############################

# TODO: Make sure, that sensitive information uses https
# TODO: Evaluate the following settings, before uncommenting them
# redirects all requests to https
# SECURE_SSL_REDIRECT = True
# session cookies will only be set, if https is used
# SESSION_COOKIE_SECURE = True
# how long is a session cookie valid?
# SESSION_COOKIE_AGE = 1209600

# validates passwords (very low security, but hey...)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# the email address, these error notifications to admins come from
# SERVER_EMAIL = str(environ.get('SERVER_MAIL'))

# how many days a password reset should work. I'd say even one day is too long
PASSWORD_RESET_TIMEOUT_DAYS = 1
