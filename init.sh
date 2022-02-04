#!/bin/sh
set -eux
python manage.py migrate
# https://docs.djangoproject.com/en/3.2/ref/django-admin/#createsuperuser
python manage.py createsuperuser --noinput
python manage.py loadproducts ledger/fixtures/products.csv
