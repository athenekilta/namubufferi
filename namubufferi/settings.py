"""
Django settings for namubufferi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
from distutils.util import strtobool

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ["DEBUG"])

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split()


# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "namubufferiapp",
    "bootstrap3",
    "autofixture",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "namubufferi.urls"

WSGI_APPLICATION = "namubufferi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/static/"

# Authentication URLs
# https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-LOGIN_URL
LOGIN_URL = "/login/"
LOGOUT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# https://www.postgresql.org/docs/9.4/static/libpq-connect.html
# https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
DATABASES["default"].update(
    dj_database_url.config(default="postgres:///namubufferi-local-test")
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATIC_URL = "/static/"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"

# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "namubufferiapp.backends.MagicAuthBackend",
]

if DEBUG == True:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # https://github.com/elbuo8/sendgrid-django
    # https://sendgrid.com/docs/Integrate/Frameworks/django.html
    # https://devcenter.heroku.com/articles/sendgrid#python
    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    SENDGRID_USER = os.environ["SENDGRID_USERNAME"]
    SENDGRID_PASSWORD = os.environ["SENDGRID_PASSWORD"]

DEFAULT_FROM_EMAIL = "namubufferi@athene.fi"
