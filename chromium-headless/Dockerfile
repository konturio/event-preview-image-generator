FROM alpine:latest

ENV \
    WIDTH=1200 \
    HEIGHT=630 \
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

#        font-wqy-zenhei \
#    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
#    echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
#    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \


COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh $WORKDIR

RUN chown -R $DOCKER_USER:$DOCKER_USER $WORKDIR && \
    chmod +x $WORKDIR/entrypoint.sh


USER $DOCKER_USER
WORKDIR $WORKDIR

EXPOSE $CDP_PORT

#ENTRYPOINT ["/bin/sh"]
ENTRYPOINT ["./entrypoint.sh"]