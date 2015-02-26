FROM  larrycai/openldap
ADD files /ldap

RUN service slapd start ;\
    cd /ldap &&\
	ldapadd -Y EXTERNAL -H ldapi:/// -f back.ldif &&\
    ldapadd -x -D cn=admin,dc=flinkwork,dc=com -w admin -c -f front.ldif &&\
    ldapadd -x -D cn=admin,dc=flinkwork,dc=com -w admin -c -f more.ldif && \
    echo "ulimit -n 1024" > /start.sh && \
    echo "slapd -h 'ldap:/// ldapi:///' -g openldap -u openldap -F /etc/ldap/slapd.d -d stats" >> /start.sh && \
    chmod +x /start.sh

EXPOSE 389
VOLUME /var/lib/ldap
CMD /start.sh
