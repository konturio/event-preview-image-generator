FROM alpine:latest

ENV \
    CDP_PORT=9222 \
    WORKDIR=/usr/src/app \
    DOCKER_USER=chromium \
    CHROME_PATH=/usr/bin/chromium-browser \
    LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

RUN set -xe && \
    apk upgrade --no-cache --available && \
    apk add --no-cache \
        ca-certificates \
        freetype \
        ttf-freefont \
        harfbuzz \
        font-noto-emoji \
        font-opensans \
        dbus \
        chromium-swiftshader \
        chromium && \
      mkdir -p $WORKDIR/.chromium && \
      adduser -D $DOCKER_USER -h $WORKDIR

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh $WORKDIR

RUN chown -R $DOCKER_USER:$DOCKER_USER $WORKDIR && \
    chmod +x $WORKDIR/entrypoint.sh


USER $DOCKER_USER
WORKDIR $WORKDIR

EXPOSE $CDP_PORT

ENTRYPOINT ["./entrypoint.sh"]