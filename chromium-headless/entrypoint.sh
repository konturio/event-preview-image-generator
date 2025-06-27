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
  --crash-dumps-dir=/tmp \
  --hide-scrollbars \
  --run-all-compositor-stages-before-draw \
  --window-size=${CHROMIUM_WIDTH:-1200},${CHROMIUM_HEIGHT:-630} \
  --remote-debugging-port=2222 \
  --user-data-dir=/app/cache/chromium \
  --disk-cache-size=${CHROMIUM_CACHE_SIZE}"

socat TCP-LISTEN:${CHROMIUM_PORT:-9222},reuseaddr,fork TCP:127.0.0.1:2222 &

/usr/bin/chromium-browser ${COMMON_SWITCHES} "$@"
