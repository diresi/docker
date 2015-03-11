#!/bin/bash
set -e
set -x

HGRC=${HOME}/.hgrc
if [ ! -f ${HGRC} ];
then
    echo "creating inital hg configuration in ${HGRC}"
    cat > ${HGRC} << EOF
[ui]
merge = internal:merge
username = Unkwown User <uu@localhost>
verbose = True

[extensions]
rebase=
mq=
graphlog=
color=
EOF

fi

cd ${HOME}
ENTE_DIR=${ENTE_DIR:-${HOME}/ente}

if [ ! -d ${ENTE_DIR} ];
then
    hg clone https://bitbucket.org/neurobase/ente ${ENTE_DIR}
else
    hg -R ${ENTE_DIR} pull --rebase
fi

hg -R ${ENTE_DIR} up -C opensource
cd ${ENTE_DIR}

scons -j1 OPT=-O2
strip ente
strip ente-tester
strip enteclient
