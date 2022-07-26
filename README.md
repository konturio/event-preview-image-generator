# Event Preview Image Generator

The project is designed to create screenshots of a web page on a browser event. Can be used to create
preview for later use when posting on social media using the opengraph protocol.

The project uses 2 containers: chromium-headless and preview-genetator. You can optionally use redis or
memcached for image caching

## [Chromium headless](chromium-headless/README.md)

## [Preview generator](preview-generator/README.md)

## Kubernetes

Create configmap

```shell
kubectl apply -f- <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: epig-config
data:
  CHROMIUM_HOST: "chromium-headless"
  CHROMIUM_PORT: "9222"
  CHROMIUM_CACHE_SIZE: "104857600"
  CHROMIUM_WIDTH: "1200"
  CHROMIUM_HEIGHT: "630"
  USE_HEADERS: "TRUE"
  SITE_URL: "https://example.com"
  EVENT_NAME: "load"
  WIDTH: "1200"
  HEIGHT: "630"
  QS: ""
  TIMEOUT: "10000"
  CACHE_URL: "redis://redis:6379"
  CACHE_PASSWORD: "redis_password"
  CACHE_TTL: "120"
  DEBUG: "FALSE"
  PORT: "8000"
EOF
```

Generate redis password

```shell
kubectl create secret generic redis-secret --from-literal=password=$(head -c 512 /dev/urandom | LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 64)
```

Apply config

```shell
kubectl apply -f ./k8s
```

## [Examples](examples/README.md)

## Disaster ninja

Configmap for Disaster ninja

```shell
kubectl apply -f- <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: epig-config
data:
  CHROMIUM_HOST: "chromium-headless"
  CHROMIUM_PORT: "9222"
  CHROMIUM_CACHE_SIZE: "104857600"
  CHROMIUM_WIDTH: "1200"
  CHROMIUM_HEIGHT: "630"
  USE_HEADERS: "FALSE"
  SITE_URL: "https://disaster.ninja/active/"
  EVENT_NAME: "event_ready_for_screenshot"
  WIDTH: "1200"
  HEIGHT: "630"
  QS: "app=f29339bd-8049-41ae-9d6b-f726d8451894"
  TIMEOUT: "60000"
  CACHE_URL: "redis://redis:6379"
  CACHE_PASSWORD: "redis_password"
  CACHE_TTL: "120"
  DEBUG: "FALSE"
  PORT: "8000"
EOF
```