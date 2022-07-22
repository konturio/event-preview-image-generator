# Preview generator

Web page screenshot service by event.

## Chromium headless

This project depends on [Chromium-headless](../chromium-headless/README.md).
You need to [build](../chromium-headless/README.md#build-image)
and [run](../chromium-headless/README.md#run-remote-debugging-protocol) Chromium headless docker container

## Setup environment variables

Create `.env` file with following variables:

* CHROMIUM_HOST - hostname of chromium-headless container
* CHROMIUM_PORT - port on which chrome debugging protocol runs (default `9222`)
* SITE_URL - website URL for screenshot
* EVENT_NAME - the name of the event after which the screenshot will be taken (default `load`)
* WIDTH - width of screenshot in pixels (default `1200`)
* HEIGHT - height of screenshot in pixels (default `630`)
* QS - additional query string parameters
* TIMEOUT - timeout in milliseconds waiting for the event (default `10000`)
* [USE_HEADERS](#custom-headers) - a boolean to listen for custom headers to set up preview-generator (default `false`)
* CACHE_URL - link to caching server (default `empty`, used in-memory cache)
* CACHE_TTL - seconds before cache expires (default `600`)
* CACHE_PASSWORD - password for redis

You can find a sample in [.env.example](.env.example)

### Custom headers

You can pass custom headers to the preview generator for dynamic customization

Matching variables table

| Environment variable | Custom header name |
|----------------------|--------------------|
| SITE_URL             | X-EPIG-url         |
| EVENT_NAME           | X-EPIG-event       |
| WIDTH                | X-EPIG-width       |
| HEIGHT               | X-EPIG-height      |
| QS                   | X-EPIG-qs          |

### Redis config variables

```dotenv
CACHE_URL='redis://localhost:6379'
CACHE_TTL=60
CACHE_PASSWORD='redis_password'
```

### Memcached config variables

```dotenv
CACHE_URL='memcached://localhost:11211'
CACHE_TTL=60
```

#### Note

Memcached does not currently work in the official release (master only) of aiocache and will be fixed in the next
release.

will be removed loop
from https://github.com/aio-libs/aiocache/blob/54dd3ed0db9b04678dc1093a9951d239f39028bb/aiocache/backends/memcached.py#L16

To enable memcached support you need to comment out `aiocache` and uncomment the following line
in [requirements.txt](requirements.txt). Also when building a docker image, you need to define build_arg
`MEMCACHED_WORKAROUND=1`

```requirements.txt
-e git+https://github.com/aio-libs/aiocache.git@master#egg=aiocache[redis,memcached]
```

## Usage

### Local run

Install requirements

```shell
pip install -r requirements.txt
pip install -r requirements.local.txt
```

Run server

```shell
export $(grep -v '^#' .env | xargs -0) 
python3 app/main.py
```

### Docker

Build image

```shell
docker build -t preview-generator:latest . 
```

Run server

```shell
docker run --rm -it -p 8000:8000 --env-file .env --link chromium-headless --name preview-generator preview-generator 
```

Open link http://localhost:8000 to get preview image
