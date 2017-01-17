#!/bin/sh

if [ "$DOCKER_MACHINE_NAME" != "namubufferi-vm" ]
then
	eval $(docker-machine env namubufferi-vm)
fi

docker-compose -f docker-files/docker-compose.yml -f docker-files/docker-compose.dev.yml exec namubufferi /usr/bin/python3 /namubufferi/manage.py collectstatic --noinput
