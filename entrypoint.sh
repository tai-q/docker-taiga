#!/bin/sh

vergt() {
    [ "$1" = "$2" ] && return 1 || [  "$2" = "`echo -e "$1\n$2" | sort -V | tail -n1`" ]
}

cd /app/taiga-back/

echo "Taiga v$TAIGA_BACK_VERSION (back) & v$TAIGA_FRONT_VERSION (front)"

if [ ! -f /data/taiga_version.txt ]; then
    echo "Initial run of taiga. Preparing..."
    python manage.py loaddata initial_user
    python manage.py loaddata initial_project_templates
    python manage.py migrate --noinput
    echo "Taiga prepared and ready to run."
else
    LAST_VERSION=$(head -1 /data/taiga_version.txt)

    if vergt $LAST_VERSION $TAIGA_BACK_VERSION; then
        echo "Taiga update detected (from v$LAST_VERSION). Updating..."
        python manage.py migrate --noinput
        echo "Taiga updated and ready to run."
    fi
fi

cd /app

python /app/conf/taiga-events/conf.py > /app/taiga-events/conf.json
python /app/conf/taiga-front/conf.py > /app/taiga-front-dist/dist/conf.json

cp /app/conf/supervisor/supervisor.conf /etc/supervisord.conf

if [ `echo $CELERY_ENABLED | tr [:upper:] [:lower:]` = "true" ]; then
    cat /app/conf/supervisor/supervisor-async.conf >> /etc/supervisord.conf
fi

if [ `echo $EVENTS_ENABLED | tr [:upper:] [:lower:]` = "true" ]; then
    cat /app/conf/supervisor/supervisor-events.conf >> /etc/supervisord.conf
fi

echo $TAIGA_BACK_VERSION > /data/taiga_version.txt

exec "$@"
