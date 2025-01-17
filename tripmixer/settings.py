"""
Django settings for tripmixer project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(f'{BASE_DIR}/.env')

SECRET_KEY = env('SECRET_KEY', default=get_random_secret_key())

DEBUG = env('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', cast=list, default=[])


# Application definition

INSTALLED_APPS = [
    'planner',
    'blog',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    "crispy_bootstrap5",
    "bootstrap_datepicker_plus",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-debug-toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']


ROOT_URLCONF = 'tripmixer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tripmixer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': env.db(default='postgresql://localhost/tripmixer')
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = f'{BASE_DIR}/staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/planner/'

LOGOUT_REDIRECT_URL = '/'

IMAGE_STORAGE_TYPE = env('IMAGE_STORAGE_TYPE', default='aws_s3')  # Options: 'aws_s3', 'storebytes'
if IMAGE_STORAGE_TYPE == 'storebytes':
    FILE_STORAGE_BACKEND = 'tripmixer.storebytes_storage.StoreBytesStorage'
elif IMAGE_STORAGE_TYPE == 'aws_s3':
    FILE_STORAGE_BACKEND = 'storages.backends.s3.S3Storage'
else:
    FILE_STORAGE_BACKEND = 'storages.backends.s3.S3Storage'

STORAGES = {
    'default': {
        'BACKEND': FILE_STORAGE_BACKEND
    },
    'staticfiles': {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

STOREBYTES_API_KEY = env('STOREBYTES_API_KEY')
STOREBYTES_API_URL = env('STOREBYTES_API_URL').rstrip('/')
STOREBYTES_BUCKET_NAME = env('STOREBYTES_BUCKET_NAME')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': env('DJANGO_LOG_FILENAME', default='django.log'),
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': env('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
    },
}
