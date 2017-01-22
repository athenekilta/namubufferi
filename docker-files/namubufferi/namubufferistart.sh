#!/bin/bash

cd /namubufferi

# Prepare log files and start outputting logs to stdout
mkdir -p /srv/logs/
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &


# This is potentially dangerous. Get the next if wrong,
# be stupid enough to use debug users in postgres
# and it'll delete production db
if [[ "$DEBUG" == true ]]
then
	# Save password for non-interactive use
	echo "postgres:5432:$POSTGRES_DB:postgres:postgres" > /.pgpass
	chmod 0600 /.pgpass
	PGPASSFILE=/.pgpass

	# Recreate db
	until dropdb -h postgres -U postgres $POSTGRES_DB
	do
		echo "Seems like db server is not ready yet."
		sleep 2
		echo "Lets retry"
	done
	createdb -h postgres -U postgres $POSTGRES_DB
	echo "DB re-created!"
fi


python3 manage.py migrate
python3 manage.py collectstatic --noinput

if [[ "$DEBUG" == true ]]
then
	# Mounting local dir will otherwise delete these files
	npm install --no-optional

	# Ensure we have superuser for development
	echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('$NAMUBUFFERI_ADMINUSER', 'admin@example.com', '$NAMUBUFFERI_ADMINPASS')" | python3 manage.py shell

	# Add some products into db
	python3 manage.py loadtestdata namubufferiapp.Category:5
	python3 manage.py loadtestdata namubufferiapp.Product:30
fi

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn3 \
	--name namubufferi \
	--bind 0.0.0.0:8080 \
	--workers $NAMUBUFFERI_GUNICORN_WORKERS \
	--reload \
	--log-level=info \
	--log-file=/srv/logs/gunicorn.log \
	--access-logfile=/srv/logs/access.log \
	namubufferi.wsgi
