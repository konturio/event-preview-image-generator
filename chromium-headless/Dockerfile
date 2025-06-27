ARG ALPINE_VERSION=3.22
FROM alpine:${ALPINE_VERSION}

RUN set -xe && \
    apk upgrade --no-cache --available && \
    apk add --no-cache \
        ca-certificates \
        freetype \
        ttf-freefont \
        harfbuzz \
        font-noto-emoji \
        font-opensans \
        chromium-swiftshader \
        chromium \
        socat \
    && \
    mkdir -p /app/cache/chromium && \
    mkdir -p /app/cache/fonts && \
    mkdir -p /app/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

WORKDIR /app/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
