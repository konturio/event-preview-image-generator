# Chromium Headless

Docker image for running Chromium in headless mode with WebGL support

## Font settings

Font settings are in the file [fonts.conf](fonts.conf) (
in [FontConfig](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html) format)

## Build image

```shell
docker build -t chromium-headless:latest . 
```

## Setup

To start chromium with http access, you need to define the following environment variables:

* CHROMIUM_ADDRESS - address (default 0.0.0.0)
* CHROMIUM_PORT - port on which chrome debugging protocol runs (default 9222)

To use Chromium's persistent cache, you need to create a volume and forward it in the docker container along the
path `/app/cache` and you need to define a variable

* CHROMIUM_CACHE_SIZE - cache size (in bytes)

To adjust the window size:

* CHROMIUM_WIDTH - window width (in pixels)
* CHROMIUM_HEIGHT - window height (in pixels)

## Usage

### Generate pdf

```shell
mkdir -p chromium-share
docker run --rm -it -v $(pwd)/chromium-share:/app/share chromium-headless --print-to-pdf=example.pdf https://example.org
```

Pdf will be saved in `chromium-share/example.pdf` file

### Generate screenshot

```shell
mkdir -p chromium-share
docker run --rm -it -v $(pwd)/chromium-share:/app/share chromium-headless --screenshot=example.png https://example.org
```

Screenshot will be saved in `chromium-share/example.png` file

### Run remote debugging protocol

To run Chromium in remote debug protocol mode

```shell
mkdir -p chromium-cache
docker run --rm -it -p 9222:9222 -e CHROMIUM_PORT=9222 -e CHROMIUM_CACHE_SIZE=104857600 -v $(pwd)/chromium-cache:/app/cache --name chromium-headless chromium-headless
```

## Testing

### Remote debugging protocol

Open a new page and go to the site - http://localhost:9222/json/new?https://example.org

List of open windows - http://localhost:9222/json

### WebGL support

To test WebGL support run following script

```shell
mkdir -p chromium-share
docker run --rm -it -v $(pwd)/chromium-share:/app/share chromium-headless --print-to-pdf=webgl.pdf https://browserleaks.com/webgl
```

and open file `chromium-share/webgl.pdf` 