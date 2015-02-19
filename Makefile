.PHONY: run-ldap run-mysql run-gerrit run

run-ldap:
	make -C ldap run

run-mysql:
	make -C mysql run

run-gerrit:
	make -C gerrit run

run: run-ldap run-mysql run-gerrit
