#
# MariaDB Dockerfile
#
# https://github.com/dockerfile/mariadb
#

# Pull base image.
FROM dockerfile/ubuntu

# Install MariaDB.
RUN \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0xcbcb082a1bb943db && \
  echo "deb http://mariadb.mirror.iweb.com/repo/10.0/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/mariadb.list && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server ldap-auth-client ldap-utils && \
  rm -rf /var/lib/apt/lists/* && \
  sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/my.cnf && \
  sed -i 's/^\(\[mysqld\]\)/\1\nplugin-load=auth-pam.so/' /etc/mysql/my.cnf && \
  echo "auth            required        pam_ldap.so config=/etc/mysql/pam_ldap.conf" > /etc/pam.d/mysql && \
  echo "account         required        pam_ldap.so config=/etc/mysql/pam_ldap.conf" >> /etc/pam.d/mysql && \
  echo "ldap_version 3" > /etc/mysql/pam_ldap.conf && \
  echo "uri ldap://ldap" >> /etc/mysql/pam_ldap.conf && \
  echo "base ou=Users,dc=flinkwork,dc=com" >> /etc/mysql/pam_ldap.conf && \
  echo "mysqld_safe &" > /tmp/config && \
  echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \"root\"@\"localhost\" WITH GRANT OPTION;'" >> /tmp/config && \
  echo "mysql -e 'INSTALL SONAME \"auth_pam.so\";'" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \"flinkwork\"@\"%\" IDENTIFIED VIA pam;'" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON \`phabricator\_%\`.* TO \"phabricator\"@\"%\" IDENTIFIED VIA pam;'" >> /tmp/config && \
  bash /tmp/config && \
  rm -f /tmp/config

# Define mountable directories.
VOLUME ["/etc/mysql", "/var/lib/mysql"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["mysqld_safe"]

# Expose ports.
EXPOSE 3306
