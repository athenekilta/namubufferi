#!/bin/bash

cd /namubufferi

while true
do
	if [[ "$NAMUBUFFERI_USELDAP" == true ]]
	then
		python3 manage.py ldap_sync_users
	fi

	sleep 300
done
