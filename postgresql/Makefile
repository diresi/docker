include ../Makefile.inc

RUN_ARGS := -p 5432:5432 -e 'DB_NAME=gitlab' -e 'DB_USER=flinkwork' -e 'DB_PASS=flinkwork'
DB_FILE = ${NAME}.flinkwork.com.${shell date +%Y%m%d-%H%M}.psql.gz
DB_LINK = ${NAME}.flinkwork.com.latest.psql.gz

backup:
	pg_dumpall -h127.0.0.1 -Upostgres | gzip > ${DB_FILE}
	ln -sf ${DB_FILE} ${DB_LINK}

restore:
	pg_restore -e -c -C -d gitlab -h127.0.0.1 -U flinkwork ${DB_LINK}
