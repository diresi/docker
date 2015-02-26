include ./Makefile.inc
.PHONY: run-ldap run-mariadb run-gerrit run

run-ldap:
	make -C ldap run

stop-ldap: stop-gerrit stop-phabricator
	make -C ldap stop

run-mariadb:
	make -C mariadb run

stop-mariadb: stop-gerrit stop-phabricator
	make -C mariadb stop

run-gerrit: run-ldap run-mariadb
	make -C gerrit run

stop-gerrit:
	make -C gerrit stop

run-phabricator: run-ldap run-mariadb
	make -C phabricator run

stop-phabricator:
	make -C phabricator stop

run: run-phabricator run-gerrit

stop: stop-ldap stop-mariadb

restart: stop run
