#!/bin/bash

cd /app/taiga-back/

python manage.py migrate --noinput
python manage.py loaddata initial_user
python manage.py loaddata initial_project_templates

cd /app

python /app/conf/taiga-events/conf.py > /app/taiga-events/conf.json
python /app/conf/taiga-front/conf.py > /app/taiga-front-dist/dist/conf.json

cp /app/conf/supervisor/supervisor.conf /etc/supervisord.conf

if [ "${CELERY_ENABLED,,}" = "true" ]; then
    cat /app/conf/supervisor/supervisor-async.conf >> /etc/supervisord.conf
fi

if [ "${EVENTS_ENABLED,,}" = "true" ]; then
    cat /app/conf/supervisor/supervisor-events.conf >> /etc/supervisord.conf
fi

exec "$@"