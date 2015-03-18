include ../Makefile.inc

DATA_DIR := /home/gerrit2/gerrit
RUN_ARGS := -p 8080:8080 -p 29418:29418 --link ldap:ldap --link mysql:mysql

_post-create-data:
	docker run --rm --volumes-from ${DATA_NAME} ${RUN_ARGS} --name ${NAME} ${TAG_NAME} bash -c 'java -jar $${GERRIT_WAR} init --batch -d $${GERRIT_HOME}/gerrit'
