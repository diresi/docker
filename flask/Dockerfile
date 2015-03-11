FROM dockerfile/ubuntu

RUN \
  sed -i 's/^# \(.*-backports\s\)/\1/g' /etc/apt/sources.list \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
     tar git curl nano wget dialog net-tools build-essential \
     ack-grep \
     python python-dev python-distribute python-pip \
     python-virtualenv \
  && adduser --disabled-login --gecos flask flask \
  && passwd -d flask \
  && gpasswd -a flask sudo \
  && sed -i 's/%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers

USER flask
WORKDIR /home/flask

EXPOSE 5000

USER flask
ENV HOME=/home/flask
VOLUME ${HOME}
RUN sudo chown -R flask.flask ${HOME}
CMD ["/home/flask/scripts/run.sh"]
