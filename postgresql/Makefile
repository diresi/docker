include ../Makefile.inc

NAME := postgresql
RUN_ARGS := -p 5432:5432 --link ldap:ldap -e 'DB_NAME=gitlab' -e 'DB_USER=flinkwork' -e 'DB_PASS=flinkwork'
DB_FILE = ${NAME}.flinkwork.com.${shell date +%Y%m%d-%H%M}.ldif
DB_LINK = ${NAME}.flinkwork.com.latest.ldif

backup: run
	pg_dump -h127.0.0.1 -U flinkwork -F c gitlab > ${DB_FILE}
	ln -sf ${DB_FILE} ${DB_LINK}

restore: run
	pg_restore -e -c -C -d gitlab -h127.0.0.1 -U flinkwork ${DB_LINK}
