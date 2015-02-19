# Phabricator (http://phabricator.org/)
#
# VERSION	1.0

FROM ubuntu:trusty
MAINTAINER Richard Osterloh, richard.osterloh@gmail.com

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git mysql-client apache2 dpkg-dev php5 libapache2-mod-php5 php5-mcrypt php5-mysql php5-gd php5-curl php-apc php5-cli php5-json ssh wget php5-ldap

# Directory for ssh
RUN mkdir /var/run/sshd

# Supervisor
RUN apt-get install -y supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/log/supervisor

RUN apt-get clean

# Enabled mod rewrite for phabticator
RUN a2enmod rewrite

ADD ./startup.sh /opt/startup.sh
RUN chmod +x /opt/startup.sh

ADD phabricator.conf /etc/apache2/sites-available/phabricator.conf
ADD apache2.conf /etc/apache2/apache2.conf
ADD local.json /opt/local.json
RUN ln -s /etc/apache2/sites-available/phabricator.conf /etc/apache2/sites-enabled/phabricator.conf
RUN rm -f /etc/apache2/sites-enabled/000-default

RUN ulimit -c 10000

EXPOSE 80 22

VOLUME /opt
CMD ["/usr/bin/supervisord"]
