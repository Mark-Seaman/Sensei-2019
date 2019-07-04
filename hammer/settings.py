"""
Django settings for sensei project.

"""

# import os
from os.path import dirname, abspath
from os.path import join

# Build paths inside the project like this: join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(BASE_DIR, 'log')
TEST_DIR = join(BASE_DIR, 'test')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# How hosts access the server
ALLOWED_HOSTS = ['seamanfamily.org', 'localhost', '127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'brain',
    'mybook',
    'tasks',
    'tool',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hammer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hammer.wsgi.application'

# Secrets
from .secret_settings import DATABASES, SECRET_KEY


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Mountain'
USE_I18N = False
USE_L10N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR + '/static',)
# STATIC_ROOT = join(BASE_DIR, 'static/')


# Login Pages

LOGIN_URL='/admin/login/'
LOGIN_REDIRECT_URL = '/'
