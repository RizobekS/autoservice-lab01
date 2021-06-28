# Python imports
from os.path import abspath, basename, dirname, join, normpath
from easy_thumbnails.conf import Settings as thumbnail_settings
import sys


# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))


# ##### APPLICATION CONFIGURATION #########################

# Apps
INSTALLED_APPS = [
    # Package apps
    'easy_thumbnails',  # Image cropping
    'image_cropping',  # Image cropping widget
    'nested_inline',  # Inlines inside inlines

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.template.context_processors',

    # Custom apps
    'apps.home',
    'apps.cars',
    'apps.services',
    'apps.accounts',

    # Package apps
    'ckeditor',  # Ckeditor
    'ckeditor_uploader',  # Ckeditor with file upload
    'django_cleanup.apps.CleanupConfig',  # Deletes old images
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

# Internationalization
LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_L10N = True

# Authentication
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'apps.accounts.backends.CaseInsensitiveModelBackend',
)


# ##### SECURITY CONFIGURATION ############################

# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# Error notification emails
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS


# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# Static dirs, root and URL
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
    join(PROJECT_ROOT, '..', 'source files'),
]
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')
STATIC_URL = '/static/'

# Media root and URL
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')
MEDIA_URL = '/media/'


# ##### DEBUG CONFIGURATION ###############################
DEBUG = False


# Grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)


# ##### PACKAGE CONFIGURATIONS ############################


# Image cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS


# CKEditor
CKEDITOR_UPLOAD_PATH = 'editor_images'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
        'height': 300,
        'width': "100%",
        'image2_disableResizer': True,
        'extraAllowedContent': '*(*)',
        'allowedContent': True,
        'extraPlugins': ','.join((
            'uploadimage',
            'autolink',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
        )),
    },
}
