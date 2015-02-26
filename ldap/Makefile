include ../Makefile.inc

NAME := ldap
RUN_ARGS := -p 389:389

LDIF_FILE = flinkwork.com.${shell date +%Y%m%d-%H%M}.ldif
LDIF_LINK = flinkwork.com.latest.ldif

backup:
	ldapsearch -b dc=flinkwork,dc=com -x -LLL -D cn=admin,dc=flinkwork,dc=com -w admin > ${LDIF_FILE}
	ln -sf ${LDIF_FILE} ${LDIF_LINK}

delete-entries:
	ldapdelete -r "dc=flinkwork,dc=com" -x -w admin -D cn=admin,dc=flinkwork,dc=com

restore: delete-entries
	ldapadd -D cn=admin,dc=flinkwork,dc=com -w admin -f ${LDIF_LINK}

search:
	ldapsearch -b ou=Users,dc=flinkwork,dc=com -x -LLL

passwd:
	read -r -p "uid: " LDAP_UID && \
	ldappasswd -D "cn=admin,dc=flinkwork,dc=com" -WS uid=$$LDAP_UID,ou=Users,dc=flinkwork,dc=com


