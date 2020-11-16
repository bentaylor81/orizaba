"""
Django settings for orizaba project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1') # Related to Celery
import django_heroku
from decouple import config
import dj_database_url
import pdfkit
import wkhtmltopdf



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['orizaba.co.uk', 'orizaba.herokuapp.com', 'localhost']


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
    'wkhtmltopdf',
    'django_filters',
    'mathfilters',
    'django_q',
    'storages',
    'app_products',
    'app_apis',
    'app_users',
    'app_orders', 
    'app_utils', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_orders.context_processors.initial_status', # LOADS INITIAL ORDER RECEIVED STATUS INTO ORDERSTATUSHISTORY TABLE
                #'app_orders.context_processors.invoice_pdf', # CREATES THE PDF INVOICE
                'app_products.context_processors.stock_movement_order', # CREATES A ROW IN STOCK MOVEMENT TABLE WHEN AN ORDER ITEM IS PURCHASED
                
                ### TEMPORARY RESET FUNCTIONS ###
                #'app_products.context_processors.stock_movement_added_false', # SET All ORDERITEMS STOCK_MOVEMENT_ADDED TO FALSE 
            ],
        },
    },
]

REST_FRAMEWORK = {
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

WSGI_APPLICATION = 'orizaba.wsgi.application'

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Uses the LIVE DB Locally
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

# # Comment out when pushing to production / Uncomment to use Live DB locally
# HEROKU_DB_KEY = config('HEROKU_DB_KEY')
# DATABASES['default'] = dj_database_url.config(default=HEROKU_DB_KEY) 

# # Comment out when pushing to production / Uncomment to use the Local DB
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

# # Local Database Settings
# DATABASES = {
# 'default': {
#     'ENGINE': config('LOCAL_DB_ENGINE'),
#     'NAME': config('LOCAL_DB_NAME'),
#     'USER': config('LOCAL_DB_USER'),
#     'PASSWORD': config('LOCAL_DB_PASSWORD'),
#     'HOST': config('LOCAL_DB_HOST'),
#     'PORT': config('LOCAL_DB_PORT'),
#     }
# }

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

#DATE_FORMAT = "d M Y"

DATETIME_FORMAT = "D d M Y - H:i"

TIME_ZONE = 'Europe/London'

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
MEDIA_ROOT = 'static/media'

# DJANGO Q - ASYNQ TASKS
Q_CLUSTER = {
    'name': 'orizaba',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': config('REDIS_HOST'),
        'password': config('REDIS_PASSWORD'),
        'port': config('REDIS_PORT'),
        'db': config('REDIS_DB'), }
}

### 3RD PARTY API CREDENTIALS ###

# HEROKU 
HEROKU_URL_CONFIG_VARS = config('HEROKU_URL_CONFIG_VARS')
HEROKU_BEARER_TOKEN = config('HEROKU_BEARER_TOKEN')

# WKHTMLTOPDF
WKHTMLTOPDF_CMD = config('WKHTMLTOPDF_CMD')

### LABEL GENERATION - CURRENTLY USED FOR PO ITEM LABEL ONLY
# WKHTMLTOPDF
WKHTMLTOPDF_CMD = config('WKHTMLTOPDF_CMD')
WKHTMLTOPDF_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
WKHTMLTOPDF_OPTIONS = {'copies' : '1', 'page-width' : '51mm', 'page-height' : '102mm', 'orientation' : 'Landscape', 'margin-top': '0', 'margin-right': '0', 'margin-bottom': '0', 'margin-left': '0', }

# PRINTNODE
PRINTNODE_URL = config('PRINTNODE_URL')
PRINTNODE_AUTH = config('PRINTNODE_AUTH')
PRINTNODE_LABEL_PRINTER = config('PRINTNODE_LABEL_PRINTER')
PRINTNODE_DESKTOP_PRINTER_HOME = config('PRINTNODE_DESKTOP_PRINTER_HOME')
PRINTNODE_DESKTOP_PRINTER_OFFICE = config('PRINTNODE_DESKTOP_PRINTER_OFFICE')
PRINTNODE_PRINT_TO_PDF = config('PRINTNODE_PRINT_TO_PDF')
PRINTNODE_HEADERS = {'Content-Type': 'application/json', 'Authorization': PRINTNODE_AUTH, }

# MAILGUN
MAILGUN_URL = config('MAILGUN_URL')
MAILGUN_AUTH = config('MAILGUN_AUTH')
MAILGUN_FROM = config('MAILGUN_FROM')
MAILGUN_BCC = config('MAILGUN_BCC')
MAILGUN_HEADERS = {'Authorization': MAILGUN_AUTH }

# SHIPTHEORY
ST_URL = config('ST_URL')
ST_URL_TOKEN = config('ST_URL_TOKEN')
ST_USERNAME = config('ST_USERNAME')
ST_PASSWORD = config('ST_PASSWORD')
ST_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': config('ST_AUTH')}

# AMAZON S3 BUCKET CONFIG
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
# Comment the above 2 lines out to use local static files
# All uploads local and live now go to AWS
# Other static files (css, pdf) are served from Heroku server

# For Environment Variables
django_heroku.settings(locals())