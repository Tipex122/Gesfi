#!/bin/bash

 NAME="gesfi"                                  # Name of the application
 DJANGODIR=/home/pi/Prog/django/gesfi             # Django project directory
 SOCKFILE=/home/pi/Prog/django/run/gunicorn.sock  # we will communicte using this unix socket
 USER=pi                                        # the user to run as
 GROUP=pi                                     # the group to run as
 NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn
 DJANGO_SETTINGS_MODULE=gesfi.settings             # which settings file should Django use
 DJANGO_WSGI_MODULE=gesfi.wsgi                     # WSGI module name

 echo "Starting $NAME as `whoami`"

 # Activate the virtual environment
 cd $DJANGODIR
 source ../venv_gesfi/bin/activate
 export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
 export PYTHONPATH=$DJANGODIR:$PYTHONPATH

 # Create the run directory if it doesn't exist
 RUNDIR=$(dirname $SOCKFILE)
 test -d $RUNDIR || mkdir -p $RUNDIR

 # Start your Django Unicorn
 # Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
  exec ../venv_gesfi/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
       --name $NAME \
       --workers $NUM_WORKERS \
       --timeout=150 \
       --user=$USER \
       --group=$GROUP \
       --bind=unix:$SOCKFILE \
       --log-level=debug \
       --log-file=-
