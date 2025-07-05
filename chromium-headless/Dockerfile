FROM debian:bookworm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        python3 python3-pip \
        fonts-freefont-ttf fonts-noto-color-emoji fonts-open-sans \
        libglvnd0 libgl1 libegl1 libvulkan1 libglx0 \
        chromium socat vulkan-tools \
    && pip3 install --no-cache-dir 'sentry-sdk>=2.32.0,<3.0.0' \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/cache/chromium /app/cache/fonts /app/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh /app/
COPY forward_logs.py /app/

RUN chmod +x /app/entrypoint.sh /app/forward_logs.py

WORKDIR /app/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
