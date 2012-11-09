#!/bin/sh
BASEDIR=$(dirname $0)/../

if [ -n "$1" ]; then
    SERVER=$1
else
    SERVER='0.0.0.0:8000'
fi

source $BASEDIR/env/bin/activate
$BASEDIR/env/bin/python $BASEDIR/project/manage.py loaddata development #Add additional fixtures here
$BASEDIR/env/bin/python $BASEDIR/project/manage.py runserver --traceback $SERVER
