.PHONY: run-ldap run-mysql run-gerrit run

run-ldap:
	make -C ldap run

stop-ldap: stop-gerrit stop-phabricator
	make -C ldap stop

run-mysql:
	make -C mysql run

stop-mysql: stop-gerrit stop-phabricator
	make -C mysql stop

run-gerrit: run-ldap run-mysql
	make -C gerrit run

stop-gerrit:
	make -C gerrit stop

run-phabricator: run-ldap run-mysql
	make -C phabricator run

stop-phabricator:
	make -C phabricator stop

run: run-phabricator run-gerrit

stop: stop-ldap stop-mysql

restart: stop run
