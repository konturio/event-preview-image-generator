FROM debian:bookworm

ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV NVIDIA_VISIBLE_DEVICES=all

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        python3 \
        python3-sentry-sdk \
        fonts-freefont-ttf fonts-noto-color-emoji fonts-open-sans \
        libvulkan1 vulkan-tools \
        libglvnd0 libegl1 libgl1 libglx0 mesa-utils \
        chromium socat \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/cache/chromium /app/cache/fonts /app/share

COPY fonts.conf /etc/fonts/local.conf
COPY entrypoint.sh /app/
COPY forward_logs.py /app/

RUN chmod +x /app/entrypoint.sh /app/forward_logs.py

WORKDIR /app/share

EXPOSE ${CHROMIUM_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
