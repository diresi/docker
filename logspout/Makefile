include ../Makefile.inc

RUN_ARGS := -p 8000:8000 -v /var/run/docker.sock:/tmp/docker.sock
#CMD_ARGS := syslog://10.0.0.1:5000

URL=${shell docker port ${NAME} 8000}
BRIDGE_IP=${shell ip addr show dev br0 | grep "inet "| sed -e "s|.*inet \(.*\)/.*|\1|"}
LOGSTASH_URL=${BRIDGE_IP}:5000

CONTAINERS := flask ente mariadb redis rabbitmq

showip:
	@echo ${BRIDGE_IP}

stream:
	curl ${URL}/logs

list:
	curl ${URL}/routes

purge:
	$(eval IDS=$(shell curl ${URL}/routes | python -c 'import sys, json; print("\n".join([route["id"] for route in json.load(sys.stdin)]))'))
	for id in ${IDS}; do \
		curl ${URL}/routes/$${id} -X DELETE; \
	done

routes: purge
	for CONTAINER in ${CONTAINERS}; do \
	    curl ${URL}/routes -X POST -d '{"source": {"filter": "'$${CONTAINER}'"}, "target": {"type": "syslog", "addr": "${LOGSTASH_URL}"}}'; \
	done
