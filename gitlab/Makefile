include ../Makefile.inc

RUN_ARGS := -p 2222:22 -p 8082:80 \
	--link redis:redisio \
	--link postgresql:postgresql \
	  -e 'DB_USER=flinkwork' \
	  -e 'DB_PASS=flinkwork' \
	  -e 'DB_NAME=gitlab' \
	--link ldap:ldapio \
	  -e 'LDAP_ENABLED=true' \
	  -e 'LDAP_HOST=ldapio' \
      -e 'LDAP_UID=uid' \
	  -e 'LDAP_BIND_DN=ou=Users,dc=flinkwork,dc=com' \
	  -e 'LDAP_BASE=ou=Users,dc=flinkwork,dc=com' \
	  -e 'LDAP_ACTIVE_DIRECTORY=false'

DATA_DIR := /home/git/data
