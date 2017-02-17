#!/bin/bash

cd /namubufferi

# Prepare log files and start outputting logs to stdout
mkdir -p /srv/logs/
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &


# While in debug mode, create a fresh database at every
# boot.
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

# Generate production statics if they do not exist
if [ ! -f "/namubufferi/webpack-stats.json" ]
then
	echo "Installing npm packages"
	npm install --no-optional
	echo "Generating static files"
	/namubufferi/node_modules/.bin/webpack --config /namubufferi/webpack.prod.config.js -p
	python3 manage.py collectstatic --noinput
fi

python3 manage.py migrate

if [[ "$DEBUG" == true ]]
then
	python3 manage.py collectstatic --noinput

	# Ensure we have superuser for development
	echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('$NAMUBUFFERI_ADMINUSER', 'admin@example.com', '$NAMUBUFFERI_ADMINPASS')" | python3 manage.py shell

	# Add some test data
	python3 manage.py loadtestdata namubufferiapp.Category:5
	python3 manage.py loadtestdata namubufferiapp.Product:30

	python3 manage.py loadtestdata auth.User:5
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
