#!/bin/sh

COMMON_SWITCHES="--headless \
  --no-sandbox \
  --disable-dev-shm-usage \
  --no-first-run \
  --disable-audio-output \
  --disable-sync \
  --disable-speech-api \
  --disable-extensions \
  --disable-features=TranslateUI \
  --disable-hang-monitor \
  --no-default-browser-check \
  --ignore-gpu-blocklist \
  --use-gl=angle \
  --use-angle=swiftshader-webgl \
  --disable-software-rasterizer \
  --disable-renderer-backgrounding \
  --disable-background-timer-throttling \
  --hide-scrollbars"

if [ -n "${CHROMIUM_PORT}" ]; then
  REMOTE_DEBUGGING="--remote-debugging-address=${CHROMIUM_ADDRESS:-0.0.0.0} --remote-debugging-port=${CHROMIUM_PORT}"
fi

if [ -n "${CHROMIUM_CACHE_SIZE}" ]; then
  CACHE_CONFIG="--user-data-dir=${WORKDIR}/cache/chromium --disk-cache-size=${CHROMIUM_CACHE_SIZE}"
fi

if [ "${CHROMIUM_WIDTH}${CHROMIUM_HEIGHT}" ]; then
  WINDOW_CONFIG="--window-size=${CHROMIUM_WIDTH:-1200},${CHROMIUM_HEIGHT:-630}"
fi

${CHROME_PATH} ${COMMON_SWITCHES} ${REMOTE_DEBUGGING} ${CACHE_CONFIG} ${WINDOW_CONFIG} $*
