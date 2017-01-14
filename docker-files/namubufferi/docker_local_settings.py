import os
import dj_database_url

SECRET_KEY = os.environ['NAMUBUFFERI_SECRETKEY']
DEBUG = True if os.environ['DEBUG'] == "true" else False

db_from_env = dj_database_url.parse(os.environ['NAMUBUFFERI_DB'])
DATABASES = {'default':db_from_env}

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

