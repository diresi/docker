#!/bin/bash
set -e
set -x

SCRIPTS=$(dirname $0)

# fetch and build ente
${SCRIPTS}/build_ente.sh

ENTE_DIR=${ENTE_DIR:-${HOME}/ente}
PYTHON=${PYTHON:-python2}

eval $(${PYTHON} -c "
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read('${HOME}/src/ente.cfg')
print ' '.join(['%s=%s' % (k.upper(), v) for k, v in cp.items('ENTE')])")

MYSQL=${MYSQL:-"mysql -h${SERVERNAME} -P${PORT} -u${USERNAME} -p${PASSWORD}"}
DB=${DB:-${DATABASE}}


# bootstrap database
echo "show databases;" | $MYSQL | grep -q ${DB} && BOOTSTRAP=0 || BOOTSTRAP=1
if [ ${BOOTSTRAP} -ne 0 ];
then
    echo "create database ${DB};" | ${MYSQL}
    ${MYSQL} ${DB} < ${ENTE_DIR}/contrib/ente_bootstrap_unicode.sql
    python2 ${ENTE_DIR}/contrib/ente_bootstrap.py --host=${SERVERNAME} --port=${PORT} --user=${USERNAME} --passwd=${PASSWORD} --db=${DB}
fi

# set up virtualenv
if [ ! -d ${HOME}/venv ];
then
    virtualenv --system venv
    source venv/bin/activate
    pip install -r ${HOME}/src/requirements.txt
fi

# install local dependencies
${SCRIPTS}/install_local_dependencies.sh

# activate venv
source ${HOME}/venv/bin/activate

# start the ente
cd ${ENTE_DIR}/contrib/minimal
${ENTE_DIR}/ente --initscript ${HOME}/src/my_init.py
