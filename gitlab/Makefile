include ../Makefile.inc

RUN_ARGS := -p 2222:22 -p 8082:80  --link postgresql:postgresql --link redis:redisio -e 'DB_USER=flinkwork' -e 'DB_PASS=flinkwork' -e 'DB_NAME=gitlab'
