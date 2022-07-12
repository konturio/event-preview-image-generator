#!/bin/sh

COMMON_SWITCHES="--headless \
  --disable-dev-shm-usage \
  --no-first-run \
  --disable-audio-output \
  --disable-sync \
  --disable-speech-api \
  --disable-extensions \
  --disable-features=TranslateUI \
  --disable-hang-monitor \
  --no-default-browser-check \
  --user-data-dir=$WORKDIR/.chromium \
  --ignore-gpu-blocklist \
  --use-gl=angle \
  --use-angle=swiftshader \
  --hide-scrollbars"

if [ -z "$*" ]; then
  REMOTE_DEBUGGING="--remote-debugging-address=0.0.0.0 --remote-debugging-port=$CDP_PORT"
fi

if ! pgrep -x "dbus-daemon" >/dev/null; then
  dbus-daemon --config-file=/usr/share/dbus-1/system.conf
else
  echo "dbus-daemon already running"
fi

$CHROME_PATH $COMMON_SWITCHES $REMOTE_DEBUGGING $*
