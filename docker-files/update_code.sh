#!/bin/sh

eval $(docker-machine env namubufferi-vm)
eval $(ssh-agent)
ssh-add ~/.docker/machine/machines/namubufferi-vm/id_rsa
docker-machine ssh namubufferi-vm mkdir -p $(pwd)

rsync -avzhe ssh --relative --delete --omit-dir-times --progress ./ docker@$(docker-machine ip namubufferi-vm):$(pwd)
rsync -avzhe ssh --delete --omit-dir-times --progress ./docker-files/namubufferi/docker_local_settings.py docker@$(docker-machine ip namubufferi-vm):$(pwd)/namubufferi/local_settings.py

