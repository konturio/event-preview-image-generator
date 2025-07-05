# Chromium Headless

Docker image for running Chromium in headless mode with WebGL or GPU support.
The container is based on Debian Bookworm so it can use the NVIDIA driver libraries injected by `nvidia-container-runtime`.

## Font settings

Font settings are in the file [fonts.conf](fonts.conf) (
in [FontConfig](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html) format)

## Build image

```shell
docker build -t chromium-headless:latest .
```
The Dockerfile installs Chromium and GPU libraries from the Debian repositories.

## Setup

To start chromium with http access, you need to define the following environment variables:

* CHROMIUM_ADDRESS - address (default 0.0.0.0)
* CHROMIUM_PORT - port on which chrome debugging protocol runs (default 9222)

To use Chromium's persistent cache, you need to create a volume and forward it in the docker container along the
path `/app/cache` and you need to define a variable

* CHROMIUM_CACHE_SIZE - cache size (in bytes)
* CHROMIUM_GPU_MODE - GPU backend selection. Allowed values:
  * `software` - default; uses SwiftShader for CPU rendering.
  * `gl` - hardware acceleration via desktop GLX.
  * `egl` - hardware acceleration via ANGLE and EGL.
  * `vulkan` - hardware acceleration via ANGLE Vulkan.

### Volumes

Bind mount the following directories if you need to persist files outside of the container:

* `/app/cache` - Chromium user data and cache
* `/app/share` - output directory for generated screenshots or pdfs

To adjust the window size, set the following optional variables:

* `CHROMIUM_WIDTH` - window width in pixels (default `1200`)
* `CHROMIUM_HEIGHT` - window height in pixels (default `630`)

### Sentry logging

Set `SENTRY_DSN` to forward Chromium logs to Sentry.
Use `SENTRY_ENV` to specify the environment name.

## Usage

### Generate pdf

```shell
mkdir -p share
docker run --rm -it -v $(pwd)/share:/app/share chromium-headless --print-to-pdf=example.pdf https://example.org
```

Pdf will be saved in `share/example.pdf` file

### Generate screenshot

```shell
mkdir -p share
docker run --rm -it -v $(pwd)/share:/app/share chromium-headless --screenshot=example.png https://example.org
```

Screenshot will be saved in `share/example.png` file

### Run remote debugging protocol

To run Chromium in remote debug protocol mode

```shell
mkdir -p cache
docker run --rm -it -p 9222:9222 -e CHROMIUM_PORT=9222 -e CHROMIUM_CACHE_SIZE=104857600 -v $(pwd)/cache:/app/cache --name chromium-headless chromium-headless
```

#### NOTE

Chrome Debugging Protocol is available only by IP address

## Testing

### Remote debugging protocol

Open a new page and go to the site - http://localhost:9222/json/new?https://example.org

List of open windows - http://localhost:9222/json

### WebGL support

To test WebGL support run following script

```shell
mkdir -p share
docker run --rm -it -v $(pwd)/share:/app/share chromium-headless --print-to-pdf=webgl.pdf https://browserleaks.com/webgl
```

and open file `share/webgl.pdf` 
