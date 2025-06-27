#!/bin/sh

COMMON_SWITCHES="--headless \
  --no-sandbox \
  --disable-gpu-sandbox \
  --disable-dev-shm-usage \
  --no-first-run \
  --disable-audio-output \
  --disable-sync \
  --disable-speech-api \
  --disable-extensions \
  --disable-features=TranslateUI,Floss,Bluetooth,MediaRouter,Sync,GcmService \
  --disable-hang-monitor \
  --no-default-browser-check \
  --ignore-gpu-blocklist \
  --use-gl=angle \
  --use-angle=swiftshader-webgl \
  --enable-unsafe-swiftshader \
  --no-default-browser-check \
  --disable-software-rasterizer \
  --disable-renderer-backgrounding \
  --disable-background-timer-throttling \
  --disable-crashpad \
  --disable-crash-reporter \
  --disable-breakpad \
  --hide-scrollbars \
  --run-all-compositor-stages-before-draw \
  --remote-debugging-port=2222 \
  --user-data-dir=/app/cache/chromium \
  --crash-dumps-dir=/tmp \  
  --window-size=${CHROMIUM_WIDTH:-1200},${CHROMIUM_HEIGHT:-630} \
  --disk-cache-size=${CHROMIUM_CACHE_SIZE}"

socat TCP-LISTEN:${CHROMIUM_PORT:-9222},reuseaddr,fork TCP:127.0.0.1:2222 &

XDG_CONFIG_HOME=/tmp/.chromium XDG_CACHE_HOME=/tmp/.chromium /usr/bin/chromium-browser ${COMMON_SWITCHES} "$@"
