#!/bin/bash
set -e

ENTE_DIR=${ENTE_DIR:-/home/ente/ente}
PYTHON=${PYTHON:-python2}

eval $(${PYTHON} -c "
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read('${HOME}/data/ente.cfg')
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

cd ${ENTE_DIR}/contrib/minimal
${ENTE_DIR}/ente --console --initscript ${HOME}/data/my_init.py
