FROM dockerfile/ubuntu

# Install Haproxy.
RUN \
  sed -i 's/^# \(.*-backports\s\)/\1/g' /etc/apt/sources.list \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
     python-mysqldb mariadb-client libqt4-xml \
     libboost-regex1.54.0 libboost-system1.54.0 libboost-filesystem1.54.0 \
     libboost-program-options1.54.0 libboost-iostreams1.54.0 libboost-python1.54.0 \
     libprotobuf8 libicu52 \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
     scons libmariadbclient-dev libqt4-dev \
     libprotobuf-dev protobuf-compiler \
     build-essential pkg-config libreadline-dev libssl-dev libncurses-dev \
     bison flex libicu-dev uuid-dev mercurial \
     libboost-python-dev libboost-regex-dev libboost-filesystem-dev \
     libboost-program-options-dev libboost-iostreams-dev \
  && rm -rf /var/lib/apt/lists/* \
  && adduser --disabled-login --gecos ente ente \
  && passwd -d ente \
  && gpasswd -a ente sudo \
  && sed -i 's/%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers

USER ente
WORKDIR /home/ente

RUN hg clone https://bitbucket.org/neurobase/ente
RUN hg -R ente up -C opensource \
    && cd ente \
    && scons -j1 OPT=-O2 \
    && strip ente \
    && strip ente-tester \
    && strip enteclient

USER root
RUN \
  DEBIAN_FRONTEND=noninteractive apt-get --purge remove -y \
     scons libmariadbclient-dev libqt4-dev \
     libprotobuf-dev protobuf-compiler \
     build-essential pkg-config libreadline-dev libssl-dev libncurses-dev \
     bison flex libicu-dev uuid-dev mercurial \
     libboost-python-dev libboost-regex-dev libboost-filesystem-dev \
     libboost-program-options-dev libboost-iostreams-dev \
  && DEBIAN_FRONTEND=noninteractive apt-get --purge autoremove -y

EXPOSE 7000

USER ente
ENV HOME=/home/ente
ADD run.sh ${HOME}/data/run.sh
ADD ente.cfg ${HOME}/data/ente.cfg
ADD my_init.py ${HOME}/data/my_init.py
RUN sudo chown -R ente.ente ${HOME}
VOLUME ${HOME}/data
CMD ["/home/ente/data/run.sh"]
