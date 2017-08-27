#!/bin/sh
python3 manage.py flush
python3 manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('$NAMUBUFFERI_ADMINUSER', 'admin@example.com', '$NAMUBUFFERI_ADMINPASS')" | python3 manage.py shell

python3 manage.py loadtestdata namubufferiapp.Category:5
python3 manage.py loadtestdata namubufferiapp.Product:30

python3 manage.py loadtestdata auth.User:5
