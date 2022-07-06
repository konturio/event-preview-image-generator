FROM python:3.9-alpine3.16

ENV WORKDIR=/app \
    DOCKER_USER=www \
    CDP_HOST='localhost' \
    CDP_PORT='9222' \
    WIDTH=1200 \
    HEIGHT=630 \
    EPIG_PORT=8000 \
    WORKER_CLASS=aiohttp.GunicornUVLoopWebWorker

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache gcc make musl-dev && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    apk --purge del gcc make musl-dev && \
    mkdir -p $WORKDIR && \
    adduser -D $DOCKER_USER -h $WORKDIR && \
    chown -R $DOCKER_USER:$DOCKER_USER $WORKDIR

COPY ./app /app

USER $DOCKER_USER
WORKDIR $WORKDIR

EXPOSE $EPIG_PORT

CMD gunicorn server:web_app --workers 1 --log-level=error --worker-class $WORKER_CLASS --bind 0.0.0.0:$EPIG_PORT
