#!/bin/sh
BASEDIR=$(dirname $0)/../

if [ -n "$1" ]; then
    SERVER=$1
else
    SERVER='0.0.0.0:8000'
fi

#source $BASEDIR/env/bin/activate
python $BASEDIR/project/manage.py collect_static
python $BASEDIR/project/manage.py migrate
#python $BASEDIR/project/manage.py loaddata development #Add additional fixtures here
python $BASEDIR/project/manage.py runserver --traceback $SERVER
