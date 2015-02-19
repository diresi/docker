.PHONY: mysql create-mysql-data run-mysql stop-mysql clean-mysql-data clean-mysql backup-mysql restore-mysql
.PHONY: ldap run-ldap stop-ldap clean-ldap create-ldap-data clean-ldap-data backup-ldap restore-ldap
.PHONY: clean

define docker_stop
	docker ps | grep '$1 *$$' >/dev/null && docker stop $1 || true
endef

define docker_rm
	docker ps -a | grep '$1 *$$' >/dev/null && docker rm -v $1 || true
endef

# mysql
mysql:
	cd mysql && docker build -t mysql .

create-mysql-data:	mysql
	docker ps -a | grep 'mysql-data *$$' || docker run --name mysql-data mysql echo "data container created"

clean-mysql-data: clean-mysql
	${call docker_rm,mysql-data}

run-mysql:	mysql clean-mysql create-mysql-data
	docker run -d --volumes-from mysql-data -p 3306:3306 --name mysql mysql

stop-mysql:
	${call docker_stop,mysql}

clean-mysql: stop-mysql
	${call docker_rm,mysql}

backup-mysql: stop-mysql
	docker run --rm --volumes-from mysql-data -v ${PWD}:/backup mysql tar cvfz /backup/mysql-data.tar.gz /var/lib/mysql

restore-mysql: stop-mysql
	docker run --rm --volumes-from mysql-data -v ${PWD}:/backup mysql tar xvfz /backup/mysql-data.tar.gz

# ldap
ldap: 
	cd ldap && docker build -t ldap .

create-ldap-data: ldap
	docker ps -a | grep 'ldap-data *$$' || docker run --name ldap-data ldap echo "data container created"

clean-ldap-data: clean-ldap
	${call docker_rm,ldap-data}

run-ldap: ldap clean-ldap create-ldap-data
	docker run -d -p 389:389 --volumes-from ldap-data --name ldap ldap

stop-ldap:
	${call docker_stop,ldap}

clean-ldap: stop-ldap
	${call docker_rm,ldap}

backup-ldap: stop-ldap
	docker run --rm --volumes-from ldap-data -v ${PWD}:/backup mysql tar cvfz /backup/ldap-data.tar.gz /var/lib/ldap

restore-ldap: stop-ldap
	docker run --rm --volumes-from ldap-data -v ${PWD}:/backup ldap tar xvfz /backup/ldap-data.tar.gz

clean:	clean-mysql clean-mysql-data clean-ldap
