#!/bin/bash
set -e
set -x

source ${HOME}/venv/bin/activate

for script in $(find ${HOME}/src -name "setup.py");
do
    (cd $(dirname ${script}) && python2 ${script} develop);
done
