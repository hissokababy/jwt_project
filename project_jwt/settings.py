"""
Django settings for project_jwt project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hmsisovuca)#1m@4#q=y_d%a&6ll$qrr+!5(zc(uj_lc8lw+)4'

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

    'jwtapp',
    'rest_framework',
    'drf_spectacular',
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

ROOT_URLCONF = 'project_jwt.urls'

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

WSGI_APPLICATION = 'project_jwt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'mypassword',
        'HOST': 'my-postgres',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "jwtapp.User"


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'jwtapp.authentication.JWTAuthentication',
    ]

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AUTH Service API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TOKEN_AUTH_HEADER = 'Bearer'


load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv('ACCESS_TOKEN_SECRET_KEY')
REFRESH_TOKEN_SECRET_KEY = os.getenv('REFRESH_TOKEN_SECRET_KEY')

HS256_ALGORITHM = 'HS256'
RS256_ALGORITHM = 'RS256'

ALGORITHMS = RS256_ALGORITHM


PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')


ACCESS_TOKEN_EXPIRE = 600
REFRESH_TOKEN_EXPIRE = (7 * 86400)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'anzorworkout@yandex.ru'
EMAIL_HOST_PASSWORD = 'amrmamapiinevknw'
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

import random

MAILING_CODE = random.randint(1111,9999)



PRIVATE_KEY = f'''-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----'''

PUBLIC_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDWL/eYHIH503PQ77ZhlXuJkBH47+p++4wudXjlFY680RYMoW06SMBySkpvLbmWBEwQaqX+rk8/oNtHSqO2YVCAS+i+I7f3zkOVLhKcRmAzOXI/sY4g063+wR4LLfRWMDKsE5K4eV5XZ7rt2W4jZ5usZliWYiuqOvMDl30OE67TUfLybdHDm/FPT2bftk32bsQSk4WBCymsAm/voefJLv9Q9xthyzEUDrYilAI0DaQ3ul2lRSBDgrK4manI5Fdzzxz5brsSUZAm0isrez8Hbq8xaz7OqjvjMDS79o1vKIDhTqcslZb/t9GzK4pI/eQ+T29fU3wDT2ahP36g3AlIKQA7jPpW+9i/0vrTC3MsVVXUXKfwl3x9rYT+2zqevOL7rPEotq6t0CTzJnx5BJsK93sYVoZwDpm2dl3siqEUv3KljomgJrzUB75yj3myNXZAoV3Cum3+LFkvVz2Bs0FxOPEV94mRJ1kA2zHkMFcBY7ySepU2Jp2HKdSLATe1BiV5P35X6nzRLpt+T8E4CMgt9Uwx9bXqJtiWeL1JVN2JOUfJv7Ddn53Uy6S8pNX90TcLS3oxNdNZYsiaDcU5/gkpp9KHFaSQvj1WVQkOZkfNVLQKa5nC41JyrJ9ci0lyODp/LdV+9s+LaFLoT71cBTbdsyFVUWRWU7n0fDdy15N3cLnA6Q== administrator@DESKTOP-2DF6KFT'
