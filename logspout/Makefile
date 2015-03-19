include ../Makefile.inc

RUN_ARGS := -p 8000:8000 -v /var/run/docker.sock:/tmp/docker.sock
#CMD_ARGS := syslog://10.0.0.1:5000

URL=${shell docker port ${NAME} 8000}

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
	curl ${URL}/routes -X POST -d '{"source": {"filter": "flask"}, "target": {"type": "syslog", "addr": "10.0.0.1:5000"}}'
	curl ${URL}/routes -X POST -d '{"source": {"filter": "ente"}, "target": {"type": "syslog", "addr": "10.0.0.1:5000"}}'
	curl ${URL}/routes -X POST -d '{"source": {"filter": "mariadb"}, "target": {"type": "syslog", "addr": "10.0.0.1:5000"}}'
	curl ${URL}/routes -X POST -d '{"source": {"filter": "redis"}, "target": {"type": "syslog", "addr": "10.0.0.1:5000"}}'
	curl ${URL}/routes -X POST -d '{"source": {"filter": "rabbitmq"}, "target": {"type": "syslog", "addr": "10.0.0.1:5000"}}'

