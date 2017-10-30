"""
Django settings for namubufferi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

def assign_from_env(name, envname, is_bool=False):
    """
    Try to read variable from enviromental variables and
    assign to name if it exists
    """
    try:
        if is_bool is True:
            evar = "False"
            if os.environ[envname] == "true":
                evar = "True"
            exec("{}={}".format(name, evar), globals())
        else:
            exec("{}='{}'".format(name, os.environ[envname]), globals())

        return True

    except KeyError:
        return False

    return False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9vzb#f%g_=!*#*j7t#!c)l2hr-$m3#s!8-+cbp3ubg&zz0tl)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'namubufferiapp',
    'bootstrap3',
    'autofixture',
    'webpack_loader',
)

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'namubufferi.urls'

WSGI_APPLICATION = 'namubufferi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

# Authentication URLs
# https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-LOGIN_URL
LOGIN_URL = '/login'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'

WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
            }
        }

# HEROKU
# Update database configuration with $DATABASE_URL.

# https://www.postgresql.org/docs/9.4/static/libpq-connect.html

# https://www.postgresql.org/message-id/21044.1326496507@sss.pgh.pa.us
# https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
#db_from_env = dj_database_url.config(default='postgres://namubufferi-local-test')
#db_from_env = dj_database_url.config(default='postgres://%2Fvar%2Flib%2Fpostgresql/namubufferi-local-test')
#db_from_env = dj_database_url.config(default='postgres://%2Fvar%2Frun%2Fpostgresql/namubufferi-local-test')
db_from_env = dj_database_url.config(default='postgres:///namubufferi-local-test')

DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_FINDERS = {
                        'django.contrib.staticfiles.finders.FileSystemFinder',
                        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
}

# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#authentication-backends
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                           'namubufferiapp.backends.MagicAuthBackend'
                           ]

if DEBUG == True:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # https://github.com/elbuo8/sendgrid-django
    # https://sendgrid.com/docs/Integrate/Frameworks/django.html
    # https://devcenter.heroku.com/articles/sendgrid#python
    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    try:
        SENDGRID_USER = os.environ['SENDGRID_USERNAME']
        SENDGRID_PASSWORD = os.environ['SENDGRID_PASSWORD']
    except:
        SENDGRID_USER = "none"
        SENDGRID_PASSWORD = "none"

# Override defaults from enviromental variables if exists
try:
    ALLOWED_HOSTS = os.environ['NAMUBUFFERI_ALLOWEDHOSTS'].split()
except KeyError:
    pass


NAMUBUFFERI_USE_SMTP = False
assign_from_env("NAMUBUFFERI_USE_SMTP", "NAMUBUFFERI_USE_SMTP", is_bool=True)
if NAMUBUFFERI_USE_SMTP == True:
    assign_from_env("EMAIL_HOST", "SMTP_HOST")
    assign_from_env("EMAIL_PORT", "SMTP_PORT")
    assign_from_env("EMAIL_HOST_USER", "SMTP_USER")
    assign_from_env("EMAIL_HOST_PASSWORD", "SMTP_PASSWORD")
    assign_from_env("EMAIL_USE_TLS", "SMTP_TLS", is_bool=True)
    assign_from_env("EMAIL_USE_SSL", "SMTP_SSL", is_bool=True)
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


assign_from_env("SECRET_KEY", "NAMUBUFFERI_SECRETKEY")
assign_from_env("DEBUG", "DEBUG", is_bool=True)
assign_from_env("STATIC_URL", "NAMUBUFFERI_STATIC_URL")

try:
    ADMIN_EMAILS = os.environ['NAMUBUFFERI_ADMIN_EMAILS'].split()
except KeyError:
    ADMIN_EMAILS = []

try:
    db_from_env = dj_database_url.parse(os.environ['NAMUBUFFERI_DB'])
    DATABASES = {'default':db_from_env}
except KeyError:
    pass


assign_from_env("OUTPAN_API_KEY", "NAMUBUFFERI_OUTPAN_API_KEY")

try:
    from namubufferi.local_settings import *
except ImportError as e:
    pass
