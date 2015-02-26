include ../Makefile.inc

NAME := postgresql
RUN_ARGS := -p 5432:5432 --link ldap:ldap -e 'DB_NAME=gitlab' -e 'DB_USER=flinkwork' -e 'DB_PASS=flinkwork'
