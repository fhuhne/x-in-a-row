FROM python:3.5

ARG DJANGO_SETTINGS_MODULE

ENV APP_DIR=/opt/app
ENV ASSET_ROOT=/tmp/fe-assets
ENV STATIC_ROOT=/opt/static

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY django/ $APP_DIR
COPY start.sh /

RUN mkdir -p $STATIC_ROOT && \
    chown -R www-data:www-data $APP_DIR $STATIC_ROOT

WORKDIR $APP_DIR

RUN pip install -r requirements/docker.txt

USER www-data

ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE:-settings.settings}

VOLUME $STATIC_ROOT
EXPOSE 8000

CMD ["/start.sh"]
