FROM debian:bookworm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        fonts-freefont-ttf fonts-noto-color-emoji fonts-open-sans \
        libglvnd0 libgl1 libegl1 libvulkan1 libglx0 \
        chromium socat vulkan-tools \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/cache/chromium /app/cache/fonts /app/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

WORKDIR /app/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
