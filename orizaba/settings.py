"""
Django settings for orizaba project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
from decouple import config
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['orizaba.herokuapp.com', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'django_filters',
    'app_websites',
    'app_apis',
    'app_users',
    'app_stats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orizaba.urls'

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
                'app_websites.context_processors.order_items', 
               # 'app_stats.context_processors.stats_sales_day', 
               # 'app_stats.context_processors.stats_sales_mon', 
               # 'app_stats.context_processors.stats_sales_year', 
            ],
        },
    },
]

WSGI_APPLICATION = 'orizaba.wsgi.application'

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Uses the LIVE DB Locally
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

# Comment out when pushing to production / Uncomment to use Live DB locally
#HEROKU_DB_KEY = config('HEROKU_DB_KEY')
#DATABASES['default'] = dj_database_url.config(default=HEROKU_DB_KEY) 

# Comment out when pushing to production / Uncomment to use the Local DB
#db_from_env = dj_database_url.config(conn_max_age=600)
#DATABASES['default'].update(db_from_env)

# Local Database Settings
#DATABASES = {
#'default': {
#    'ENGINE': config('LOCAL_DB_ENGINE'),
#    'NAME': config('LOCAL_DB_NAME'),
#    'USER': config('LOCAL_DB_USER'),
#    'PASSWORD': config('LOCAL_DB_PASSWORD'),
#    'HOST': config('LOCAL_DB_HOST'),
#    'PORT': config('LOCAL_DB_PORT'),
#   }
#}
 
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

DATE_FORMAT = "d M Y"

DATETIME_FORMAT = "d M Y - H:i:s"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [							
                    os.path.join(BASE_DIR, 'static'),
                ]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files # 

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# For Environment Variables
django_heroku.settings(locals())