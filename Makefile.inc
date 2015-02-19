REPO := flinkwork
.PHONY: build run stop create-data clean-data clean raw-backup raw-restore

TAG_NAME = ${REPO}/${NAME}
DATA_NAME = ${NAME}-data
RUN_ARGS :=
DATA_DIR = /var/lib/${NAME}

BACKUP_DIR  = /backup
BACKUP_FILE = ${BACKUP_DIR}/${NAME}-${shell date +%Y%m%d-%H%M}.tar.gz
BACKUP_LINK = ${BACKUP_DIR}/${NAME}-latest.tar.gz

define docker_stop
	docker ps | grep '$1 *$$' >/dev/null && docker stop $1 || true
endef

define docker_rm
	docker ps -a | grep '$1 *$$' >/dev/null && docker rm -v $1 || true
endef

build:
	docker build -t ${TAG_NAME} .

create-data:
	docker ps -a | grep '${DATA_NAME} *$$' || docker run --name ${DATA_NAME} ${TAG_NAME} echo "data container '${DATA_NAME}' created"

clean-data: clean
	${call docker_rm,${DATA_NAME}}

run: build clean create-data
	docker run -d --volumes-from ${DATA_NAME} ${RUN_ARGS} --name ${NAME} ${TAG_NAME}

run-bash: build clean create-data
	docker run --rm -it --volumes-from ${DATA_NAME} ${RUN_ARGS} --name ${NAME} ${TAG_NAME} bash

stop:
	${call docker_stop,${NAME}}

clean: stop
	${call docker_rm,${NAME}}

show-data-dir:
	@echo ${DATA_DIR}

raw-backup: stop
	docker run --rm --volumes-from ${DATA_NAME} -v ${PWD}:${BACKUP_DIR} ${TAG_NAME} bash -c 'tar cfz ${BACKUP_FILE} ${DATA_DIR} && \
																						ln -sf ${BACKUP_FILE} ${BACKUP_LINK}'

raw-restore: stop
	docker run --rm --volumes-from ${DATA_NAME} -v ${PWD}:${BACKUP_DIR} ${TAG_NAME} tar xfz ${BACKUP_LINK}

bash:
	docker exec -it ${NAME} bash

// vim: filetype=make