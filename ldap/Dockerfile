FROM  larrycai/openldap
ADD files /ldap

RUN service slapd start ;\
    cd /ldap &&\
	ldapadd -Y EXTERNAL -H ldapi:/// -f back.ldif &&\
    ldapadd -x -D cn=admin,dc=flinkwork,dc=com -w admin -c -f front.ldif &&\
    ldapadd -x -D cn=admin,dc=flinkwork,dc=com -w admin -c -f more.ldif

EXPOSE 389
VOLUME /var/lib/ldap
