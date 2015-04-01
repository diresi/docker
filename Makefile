include Makefile.inc

.PHONY: startall stopall killall

APP_CONTAINERS := mariadb redis rabbitmq ente flask
LOG_CONTAINERS := elasticsearch logstash kibana logspout

startapp:
	for CONTAINER in ${APP_CONTAINERS}; do \
		make -C $${CONTAINER} start; \
	done

startlog:
	for CONTAINER in ${LOG_CONTAINERS}; do \
		make -C $${CONTAINER} start; \
	done

stopall:
	find ${CURDIR} -maxdepth 1 -type d -exec make -C '{}' stop \;

killall:
	find ${CURDIR} -maxdepth 1 -type d -exec make -C '{}' kill \;
