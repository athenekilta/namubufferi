#!/bin/sh

if docker-machine create -d virtualbox namubufferi-vm
then
	docker-machine stop namubufferi-vm
	VBoxManage sharedfolder add namubufferi-vm --name projecthome --automount --hostpath $(pwd)
	VBoxManage setextradata namubufferi-vm VBoxInternal2/SharedFoldersEnableSymlinksCreate/projecthome 1
fi
docker-machine start namubufferi-vm

docker-machine ssh namubufferi-vm -- sudo umount $(pwd)
docker-machine ssh namubufferi-vm -- mkdir -p $(pwd)
docker-machine ssh namubufferi-vm -- sudo mount --bind /projecthome $(pwd)

echo ""
echo "Now run eval \$(docker-machine env namubufferi-vm)"
