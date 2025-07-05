FROM ubuntu:24.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libglvnd0 libgl1 libegl1 libvulkan1 libglx0 \
        chromium-browser fonts-noto-color-emoji socat vulkan-tools \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/cache/chromium /app/cache/fonts /app/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

WORKDIR /app/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
