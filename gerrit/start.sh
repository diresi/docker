#!/bin/bash

set -e

MYSQL_INIT_FILE=${GERRIT_HOME}/mysql_initialized

if [ ! -f ${MYSQL_INIT_FILE} ];
then
    java -jar ${GERRIT_WAR} init --batch -d ${GERRIT_HOME}/gerrit
    touch ${MYSQL_INIT_FILE}
fi


$GERRIT_HOME/gerrit/bin/gerrit.sh run
