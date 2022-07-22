ARG ALPINE_VERSION=3.16
FROM alpine:${ALPINE_VERSION}

ENV WORKDIR=/app \
    CHROME_PATH=/usr/bin/chromium-browser

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
        mkdir -p ${WORKDIR}/cache && \
        mkdir -p ${WORKDIR}/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh ${WORKDIR}

RUN chmod +x ${WORKDIR}/entrypoint.sh

WORKDIR ${WORKDIR}/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["../entrypoint.sh"]
