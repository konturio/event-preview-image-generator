#!/bin/sh


# Select GPU backend.
# 'software' - SwiftShader CPU rendering (default).
# 'gl'       - Desktop GLX acceleration.
# 'egl'      - EGL hardware acceleration.
# 'vulkan'   - Vulkan hardware acceleration.
GPU_MODE=${CHROMIUM_GPU_MODE:-software}

# Base list of Chromium features to disable. Will be amended depending on GPU mode.
DISABLE_FEATURES="TranslateUI,Floss,Bluetooth,MediaRouter,Sync,GcmService"

case "$GPU_MODE" in
  vulkan)
    GPU_SWITCHES="--use-angle=vulkan \
      --enable-features=Vulkan,UseSkiaRenderer \
      --disable-vulkan-surface"
    ;;
  egl)
    DISABLE_FEATURES="${DISABLE_FEATURES},Vulkan"
    GPU_SWITCHES="--use-angle=gl-egl \
      --use-gl=egl \
      --use-cmd-decoder=passthrough"
    ;;
  gl)
    DISABLE_FEATURES="${DISABLE_FEATURES},Vulkan"
    GPU_SWITCHES="--use-gl=desktop"
    ;;
  *)
    DISABLE_FEATURES="${DISABLE_FEATURES},Vulkan"
    GPU_SWITCHES="--use-gl=angle \
      --use-angle=swiftshader-webgl \
      --enable-unsafe-swiftshader"
    ;;
esac

# Compose common Chromium switches after GPU mode is processed so that
# DISABLE_FEATURES includes any amendments.
COMMON_SWITCHES="--headless \
  --no-sandbox \
  --disable-gpu-sandbox \
  --disable-dev-shm-usage \
  --no-first-run \
  --disable-audio-output \
  --disable-sync \
  --disable-speech-api \
  --disable-extensions \
  --disable-hang-monitor \
  --no-default-browser-check \
  --ignore-gpu-blocklist \
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
  --disk-cache-size=${CHROMIUM_CACHE_SIZE} \
  --disable-features=${DISABLE_FEATURES}"

socat TCP-LISTEN:${CHROMIUM_PORT:-9222},reuseaddr,fork TCP:127.0.0.1:2222 &

XDG_CONFIG_HOME=/tmp/.chromium XDG_CACHE_HOME=/tmp/.chromium \
  /usr/bin/chromium ${COMMON_SWITCHES} ${GPU_SWITCHES} "$@"
