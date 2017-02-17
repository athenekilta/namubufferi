#!/bin/bash

# Wait for the initial setup. Not waiting wouldn't be dangerous, but
# it will show a long error message in the log when the db isn't ready
# yet.
sleep 20

cd /namubufferi

while true
do
	if [[ "$NAMUBUFFERI_USELDAP" == true ]]
	then
		python3 manage.py ldap_sync_users
	fi

	sleep 300
done
