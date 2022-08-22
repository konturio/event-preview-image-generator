# Preview generator

Web page screenshot service by event.

## Chromium headless

This project depends on [Chromium-headless](../chromium-headless/README.md).
You need to [build](../chromium-headless/README.md#build-image)
and [run](../chromium-headless/README.md#run-remote-debugging-protocol) Chromium headless docker container

## Setup environment variables

You can find a sample in [.env.example](.env.example)

```shell
cp .env.example .env
```

Edit `.env` file with following variables:

* CHROMIUM_HOST - hostname of chromium-headless container
* CHROMIUM_PORT - port on which chrome debugging protocol runs (default `9222`)
* SITE_URL - website URL for screenshot
* EVENT_NAME - the name of the event after which the screenshot will be taken (default `load`)
* WIDTH - width of screenshot in pixels (default `1200`)
* HEIGHT - height of screenshot in pixels (default `630`)
* IMAGE_FORMAT - format of screenshot: png or jpeg (default `png`)
* QS - additional query string parameters (overrides specified parameters from the available query string)
* DEFAULT_IMAGE_URL - image url to display on timeout error (default `empty`). You need to create default image with the
  same width, height and image format 
* ALLOW_EMPTY_QS - generate screenshot when query string is empty, otherwise returns an error or DEFAULT_IMAGE_URL if
  present (default `TRUE`)
* TIMEOUT - timeout in milliseconds waiting for the event (default `10000`)
* [USE_HEADERS](#custom-headers) - a boolean to listen for custom headers to set up preview-generator (default `false`)
* CACHE_URL - link to caching server (default `empty`, disable cache)
* CACHE_TTL - seconds before cache expires (default `600`)
* CACHE_PASSWORD - password for redis

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

### Caching

In-memory cache

```dotenv
CACHE_URL='memory://'
CACHE_TTL=60
```

Redis config variables

```dotenv
CACHE_URL='redis://localhost:6379'
CACHE_TTL=60
CACHE_PASSWORD='redis_password'
```

## Usage

### Local run

Install requirements

```shell
pip install -r requirements.txt
```

Run server

```shell
export $(grep -v '^#' .env | xargs -0) 
python3 app/main.py
```

### Docker

Override `CHROMIUM_HOST` variable to `chromium`

```shell
find ./.env -type f -exec sed -i '' -e 's/CHROMIUM_HOST=localhost/CHROMIUM_HOST=chromium/g' {} \;
```

Build image

```shell
docker build -t preview-generator:latest . 
```

Run server

```shell
docker run --rm -it -p 8000:8000 --env-file .env --link chromium-headless:chromium --name preview-generator preview-generator 
```

Open link http://localhost:8000 to get preview image

### Liveness route

You can use health check to detect if an application is running. It is available via the `/health` route, which responds
with HTTP code 200. 