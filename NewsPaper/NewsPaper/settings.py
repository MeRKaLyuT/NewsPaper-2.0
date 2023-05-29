"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/

"""
import os
from pathlib import Path
import redis
import logging


logger = logging.getLogger(__name__)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i8zhoy=11w4&5dz5*!y+u8!b#x#7oagqc+v%rw-f*z!)0r-9@5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'news.apps.NewsConfig',
    'django_filters',
    # подключение авторизации через другие сайты
    # обязательно django.contrib.sites/messages/auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    # для периодичных задач | pip install django-apscheduler
    'django_apscheduler',
    'django_dump_load_utf8',
]

MIDDLEWARE = [
    # Чем выше в списке, тем выше слой, а значит, и SecurityMiddleware должен быть как можно выше
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',


]

ROOT_URLCONF = 'NewsPaper.urls'
LOGIN_REDIRECT_URL = '/news'
# чтобы allauth распознал форму как ту, что должна выполняться вместо формы по умолчанию, необходимо добавить это
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignUpForm"}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # обязательная часть авторизации через другие приложения
                'django.template.context_processors.request',
                # ------------------------------------------
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

SITE_ID = 1

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
# Тоже для авторизации через allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '48973306m.',
        'HOST': 'Localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Регистрация по email и паролю. D5.4
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# mandatory - без подтверждения не пустит. Optional - пропустит и без подтверждения
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# после подтверждения почты сразу заходит в аккаунт
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# хранит дни, сколько доступно для активации почты
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS

# Отправка писем на почту
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = "kiparenko06@mail.ru"
EMAIL_HOST_PASSWORD = "yUfsnGaWNK0vuxakDRbk"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# yUfsnGaWNK0vuxakDRbk

DEFAULT_FROM_EMAIL = "kiparenko06@mail.ru"


# для отправки писем админам об авторизации пользователя
SERVER_EMAIL = 'kiparenko06@mail.ru'
ADMINS = (
    ('Maxim', 'kiparenko06@mail.ru'),
    ('Vlada', 'vlada-kalina@mail.ru')
)
MANAGERS = (
    ('Maxim', 'kiparenko06@mail.ru'),
    ('Vlada', 'vlada-kalina@mail.ru')
)
EMAIL_SUBJECT_PREFIX = ''
SITE_URL = 'http://127.0.0.1:8000'


CELERY_BROKER_URL = f'redis://default:eTjtcrIxBKPGnOwQ5Cp3iwkVFM6r4bGb@redis-14075.c55.eu-central-1-1.ec2.cloud.redislabs.com:14075'

CELERY_RESULT_BACKEND = f'redis://default:eTjtcrIxBKPGnOwQ5Cp3iwkVFM6r4bGb@redis-14075.c55.eu-central-1-1.ec2.cloud.redislabs.com:14075'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT':  30,
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',
    'formatters': {
        'debugsimple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'warning': {
          'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s'
        },
        'errorandcrit': {
            'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s %(exc_info)s'
        },
        'info': {
            'format': '%(levelname)s %(module)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debugsimple',
            'filters': ['require_debug_true'],
        },
        'InfoLog': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'info',
            'filters': ['require_debug_false'],
        },
        'WarningLog': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'warning',
            'filters': ['require_debug_true'],
        },
        'ErrorCriticalLogCon': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'errorandcrit',
            'filters': ['require_debug_true'],
        },
        'ErrorCriticalLog': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'errorandcrit'
        },
        'security': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'info',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'warning',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['InfoLog', 'console', 'WarningLog', 'ErrorCriticalLogCon', ],
            'propagate': True,
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['ErrorCriticalLog', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.server': {
            'handlers': ['ErrorCriticalLog', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.template': {
            'handlers': ['ErrorCriticalLog', ],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['ErrorCriticalLog', ],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['security', ],
            'propagate': True,
            'level': 'DEBUG',
        },

    }
}
