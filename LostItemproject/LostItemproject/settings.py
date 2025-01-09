"""
Django settings for LostItemproject project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

from pathlib import Path
from django.db import connection
from django.db.backends.signals import connection_created
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!=h=1#zx36nys&0lxm9gwr6(6rpg36l--t2q@jn8$3f69i3h+4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'top',
    'lostitem',
    'founditem',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LostItemproject.urls'

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
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'LostItemproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


def enable_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        connection.cursor().execute('PRAGMA foreign_keys = ON;')


# Connection signals, enable foreign key constraints
connection_created.connect(enable_foreign_keys)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django',  # database name
#         'HOST': '127.0.0.1',  # mysql host
#         'PORT': 3306,  # mysql port
#         'USER': 'root',  # mysql username
#         'PASSWORD': '123456'  # mysql password
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Path where uploaded media files are stored
SITE_DOMAIN = "127.0.0.1:8000"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '1528392308@qq.com'
EMAIL_HOST_PASSWORD = 'eqlatyyhvtombagd'

DEFAULT_FROM_EMAIL = '1528392308@qq.com'


# Celery config
# You can start Redis with the command redis-server
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis ss a message queue
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TASK_SERIALIZER = "pickle"
# CELERY_ACCEPT_CONTENT = ["json", "pickle"]
# CELERY_RESULT_SERIALIZER = "pickle"

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Tokyo'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_BEAT_SCHEDULE = {
#     'sample_task': {
#         'task': 'founditem.tasks.my_scheduled_task',
#         'schedule': crontab(minute='*/1'),  # 每分钟运行一次
#     },
# }

# 这里是由于图片在Gmail上的展示问题，暂时使用GITHUB的图片展示，后面替换为项目的地址
# こちらはGmailでの画像表示の問題による一時的な対応として、現在GitHubの画像リンクを使用しています。後ほどプロジェクトのアドレスに置き換える予定です。
IMAGE_BASE_URL = 'https://raw.githubusercontent.com/Krat1078/Revised_Yugou_2024_teamB/refs/heads/main/LostItemproject/'