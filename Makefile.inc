REPO := flinkwork
.PHONY: build run start stop kill create-data drop-data clean raw-backup raw-restore drop-image clean-images clean-containers
.PHONY: log logf

NAME = ${shell basename ${CURDIR}}
TAG_NAME = ${REPO}/${NAME}
DATA_NAME = ${NAME}-data
RUN_ARGS :=
CMD_ARGS :=
DATA_DIR = /var/lib/${NAME}

BACKUP_DIR  = /backup
BACKUP_FILE = ${BACKUP_DIR}/${NAME}-${shell date +%Y%m%d-%H%M}.tar.gz
BACKUP_LINK = ${BACKUP_DIR}/${NAME}-latest.tar.gz

define docker_stop
	docker ps | grep '$1 *$$' >/dev/null && docker stop $1 || true
endef

define docker_kill
	docker ps | grep '$1 *$$' >/dev/null && docker kill $1 || true
endef

define docker_rm
	docker ps -a | grep '$1 *$$' >/dev/null && docker rm -v $1 || true
endef

build:
	docker build -t ${TAG_NAME} .

create-data:
	docker ps -a | grep '${DATA_NAME} *$$' || docker run --name ${DATA_NAME} ${RUN_ARGS} --entrypoint echo ${TAG_NAME} "data container '${DATA_NAME}' created"

drop-data: clean
	${call docker_rm,${DATA_NAME}}

run: build clean create-data
	docker run -d --volumes-from ${DATA_NAME} ${RUN_ARGS} --name ${NAME} ${TAG_NAME} ${CMD_ARGS}

show-run:
	@echo docker run -d --volumes-from ${DATA_NAME} ${RUN_ARGS} --name ${NAME} ${TAG_NAME} ${CMD_ARGS}

start: run

run-bash: build clean create-data
	docker run --rm -it --volumes-from ${DATA_NAME} ${RUN_ARGS} --entrypoint bash --name ${NAME} ${TAG_NAME}

stop:
	${call docker_stop,${NAME}}

kill:
	${call docker_kill,${NAME}}

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

clean-images:
	for h in $$(docker images | grep "^<none>" | sed -re "s/(\S+\s+){2}(\S+).*/\2/"); do \
		docker rmi $$h; \
	done

clean-containers:
	for c in $$(docker ps -aq); do \
		docker rm -v $$c; \
	done

drop-image: drop-data
	docker rmi ${TAG_NAME}

log:
	docker logs ${NAME}

logf:
	docker logs -f ${NAME}

// vim: filetype=make
