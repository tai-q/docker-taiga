FROM python:3.6-alpine

EXPOSE 80
VOLUME /data
HEALTHCHECK CMD curl http://127.0.0.1/conf.json && curl http://127.0.0.1/api/v1/ || exit 1

ENV TAIGA_BACK_VERSION 4.2.12
ENV TAIGA_FRONT_VERSION 4.2.13-stable
ENV TAIGA_LDAP_VERSION 0.4.4
ENV TAIGA_EVENTS_VERSION 2de073c1a3883023050597a47582c6a7405914de

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

RUN set -x \
    && addgroup -S -g 105 app \
    && adduser -h /app -S -D -H -u 105 app app \
    && apk update \
    && apk add \
        nginx \
        git \
        nodejs \
        npm \
        gettext \
        gcc \
        libpq\
        libjpeg \
        libxslt \
        musl-dev \
        libffi-dev \
        postgresql-dev \
        libxslt-dev \
        zlib-dev \
        jpeg-dev \
    && mkdir /run/nginx/ \
    && touch /run/nginx/nginx.pid \
    && pip install --no-cache-dir supervisor \
    && git clone https://github.com/taigaio/taiga-front-dist -b ${TAIGA_FRONT_VERSION} \
    && git clone https://github.com/taigaio/taiga-back -b ${TAIGA_BACK_VERSION} \
    && git clone https://github.com/taigaio/taiga-events \
    && cd taiga-events && git reset --hard ${TAIGA_EVENTS_VERSION} && cd ../ \
    && rm -rf ./*/.git \
    && rm -rf /var/cache/apk/* \
    && pip install --no-cache-dir -r taiga-back/requirements.txt \
    && pip install --no-cache-dir taiga-contrib-ldap-auth-ext==${TAIGA_LDAP_VERSION} \
    && cd taiga-back && python manage.py compilemessages && cd ../ \
    && cd taiga-back && python manage.py collectstatic --noinput && cd ../ \
    && cd taiga-events && npm install -y && cd ../ \
    && apk del git npm gettext gcc musl-dev libffi-dev postgresql-dev libxslt-dev zlib-dev jpeg-dev

COPY conf/ /app/conf/
COPY entrypoint.sh /app/

RUN set -x \
    && ln -sf /app/conf/nginx/taiga.conf /etc/nginx/conf.d/default.conf \
    && ln -sf /app/conf/taiga-back/local.py /app/taiga-back/settings/local.py \
    && ln -sf /app/conf/taiga-back/env-settings.py /app/taiga-back/settings/env.py \
    && ln -sf /app/conf/taiga-back/celery_local.py /app/taiga-back/settings/celery_local.py \
    && ln -sf /app/conf/taiga-back/celery-settings.py /app/taiga-back/settings/celery_settings.py \
    && chmod u+x /app/entrypoint.sh \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["supervisord"]
