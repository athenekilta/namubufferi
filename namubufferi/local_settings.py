import os
import dj_database_url

if os.environ['NAMUBUFFERI_SECRETKEY']:
    SECRET_KEY = os.environ['NAMUBUFFERI_SECRETKEY']

DEBUG = True if os.environ['DEBUG'] == "true" else False

if os.environ['NAMUBUFFERI_DB']:
    db_from_env = dj_database_url.parse(os.environ['NAMUBUFFERI_DB'])
    DATABASES = {'default':db_from_env}

if os.environ['NAMUBUFFERI_STATIC_URL']:
    STATIC_URL = os.environ['NAMUBUFFERI_STATIC_URL']
if os.environ['NAMUBUFFERI_STATIC_ROOT']:
    STATIC_ROOT = os.environ['NAMUBUFFERI_STATIC_ROOT']

