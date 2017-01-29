#!/bin/bash

if [[ "$DEBUG" == "true" ]] && [[ ! -e "/ldapready" ]]
then

        # Recreate db
        until ldapadd -h localhost -p 389 -c -x -D cn=admin,dc=namubufferidomain,dc=com -w rootpass -f /fixtures.ldif
        do
		if [[ $? == 68 ]]
		then
			echo "Fixtures already existed"
			touch "/ldapready"

			exit 1
		fi

                echo "Seems like ldap server is not ready yet."
                sleep 2
                echo "Lets retry"
        done

	touch "/ldapready"
        echo "LDAP fixtures added!"
fi

while true
do
	sleep 10
done
