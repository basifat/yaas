"""
Django settings for yaas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTH_PROFILE_MODULE = "accounts.UserProfile"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i+e#hyfrit&9amii*4=5c+_q%=l3c7itn2$nd19at1)+mf+d(r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_FROM_EMAIL = "Yaas Application Website <babatunde@gmail.com>"

EMAIL_HOST = "smtp.gmail.com"#'smtp.sendgrid.net'
EMAIL_HOST_USER = "babatunde.asifat@gmail.com"
EMAIL_HOST_PASSWORD = "odabzkvprasznkjf"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

SITE_URL = "http://127.0.0.1:8000/"
if DEBUG:
    SITE_URL = "http://127.0.0.1:8000"




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'accounts',
    'auctions',
    'djcelery',
    'kombu.transport.django',
    'django_cron',
    'django.contrib.staticfiles',
    'tastypie',
    #'debug_toolbar',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auctions.description.GetAllAuction',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auctions.description.GetAllAuction',
)

CRON_CLASSES = [
    "yaas.cron.MyCronJob",
    # ...
]

ROOT_URLCONF = 'yaas.urls'

WSGI_APPLICATION = 'yaas.wsgi.application'

SOUTH_TESTS_MIGRATE = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",  
)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
#look for static and media folder in the folder above where manage.py is located
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'media') 
#MEDIA_ROOT = 'D:\SchoolWork\Webservices\ecommerce\static\media/'
#template folder stored in project root
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'static_root') 
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'static', 'static_files'), 
    )
TEMPLATE_DIRS = ( 
            os.path.join(BASE_DIR, 'templates'),
    )

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#app.conf.update(
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
#)


#app.conf.update(
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
#

#celery = Celery(broker="amqp://guest:guest@127.0.0.1:6379//")

#celery.conf.update(
#BROKER_URL = "redis://localhost:6379/"
#CELERY_DEFAULT_QUEUE = "yaas",
#CELERY_DEFAULT_EXCHANGE = "yaas",
#CELERY_DEFAULT_EXCHANGE_TYPE = "direct",
#CELERY_DEFAULT_ROUTING_KEY = "yaas",
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
#)
