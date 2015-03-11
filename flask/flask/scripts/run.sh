#!/bin/bash
set -e
set -x

SCRIPTS=$(dirname $0)

# set up virtualenv
if [ ! -d ${HOME}/venv ];
then
    virtualenv --system venv
fi

# activate venv
source ${HOME}/venv/bin/activate
pip install -r ${HOME}/src/requirements.txt

# install local dependencies
${SCRIPTS}/install_local_dependencies.sh

# start our app
python ${HOME}/src/app.py
