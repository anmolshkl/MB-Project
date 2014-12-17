#!/bin/bash
set -e
LOGFILE=/home/anmolshkl/repo/MB-beta1/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=root
GROUP=root
ADDRESS=127.0.0.1:8001
cd /home/anmolshkl/repo/MB-beta1
source /home/anmolshkl/repo/MB-beta1/env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn mentorbuddy.wsgi:application --bind=127.0.0.1:8001
#exec sudo gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS --user=$USER --group=$GROUP --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE 