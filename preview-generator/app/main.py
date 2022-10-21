from typing import TYPE_CHECKING
import socket
import hashlib
import ujson as json
from aiocache import cached, caches
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import Response, RedirectResponse, PlainTextResponse
from starlette.exceptions import HTTPException
from starlette.datastructures import QueryParams, URL
from pyppeteer.errors import BrowserError, PageError
from settings import Settings
from secret import Secret
from epig import EventPreviewImageGenerator, TimeoutError
from cache_config import cache_config
from logger import LOGGER

if TYPE_CHECKING:
    from starlette.requests import Request

settings = Settings()
secret = Secret()


app = Starlette()

if settings.CACHE_URL != '':
    caches.set_config(cache_config(settings.CACHE_URL, secret.CACHE_PASSWORD))


def cache_key_builder(f, current_settings: 'Settings') -> str:
    key = {
        'module': f.__module__,
        'func': f.__name__,
        **current_settings.asdict()
    }
    return hashlib.md5(json.dumps(key).encode("utf-8")).hexdigest()


async def default_image(default_image_url: URL):
    if default_image_url:
        return RedirectResponse(url=default_image_url, status_code=307)
    raise HTTPException(status_code=404)


async def screenshot(current_settings: 'Settings') -> bytes:
    # Fix problem with DNS. Chromium debug protocol refuses access by dns name
    ip_addr = socket.gethostbyname(current_settings.CHROMIUM_HOST)
    browserUrl = str(URL(scheme='http', hostname=ip_addr, port=current_settings.CHROMIUM_PORT))
    LOGGER.debug('Resolved IP of chromium host %s', ip_addr)
    LOGGER.debug('trying to connect to %s', browserUrl)

    epig = await EventPreviewImageGenerator.create(
        # str(URL(scheme='http', hostname=current_settings.CHROMIUM_HOST, port=current_settings.CHROMIUM_PORT)),
        browserUrl,
        current_settings.WIDTH,
        current_settings.HEIGHT,
        timeout=current_settings.TIMEOUT,
        debug=current_settings.DEBUG
    )
    try:
        return await epig.screenshot(
            str(current_settings.SITE_URL),
            event_name=current_settings.EVENT_NAME,
            image_type=current_settings.IMAGE_FORMAT
        )
    finally:
        await epig.close()


@app.route("/active/preview.png", methods=["GET"])
async def preview(request: 'Request') -> 'Response':
    current_settings = settings.copy()

    # Rewrite variables by headers
    if current_settings.USE_HEADERS:
        headers = Config(environ=request.headers)
        current_settings = Settings(
            SITE_URL=headers('X-EPIG-url', cast=URL, default=str(Settings.SITE_URL)),
            EVENT_NAME=headers('X-EPIG-event', cast=str, default=Settings.EVENT_NAME),
            WIDTH=headers('X-EPIG-width', cast=int, default=Settings.WIDTH),
            HEIGHT=headers('X-EPIG-height', cast=int, default=Settings.HEIGHT),
            QS=headers('X-EPIG-qs', cast=QueryParams, default=str(Settings.QS))
        )

    LOGGER.debug('Current settings %s', current_settings)
    # On empty query string and ALLOW_EMPTY_QS=False
    if not current_settings.ALLOW_EMPTY_QS and not request.query_params:
        LOGGER.debug('ALLOW_EMPTY_QS=False and query_string is empty. Returning DEFAULT_IMAGE_URL')
        return await default_image(current_settings.DEFAULT_IMAGE_URL)

    # Update SITE_URL with query_string
    current_settings.SITE_URL = current_settings.SITE_URL.include_query_params(
        **dict(request.query_params)
    ).include_query_params(
        **dict(current_settings.QS)
    )

    # Add cache decorator if cache enabled
    screenshot_cached = cached(
        namespace="epig",
        ttl=current_settings.CACHE_TTL,
        alias='default',
        key_builder=cache_key_builder
    )(screenshot) if current_settings.CACHE_URL != '' else screenshot

    try:
        img = await screenshot_cached(current_settings)
        return Response(content=img, media_type="image/" + current_settings.IMAGE_FORMAT)
    except BrowserError:
        raise HTTPException(status_code=503)
    except PageError:
        raise HTTPException(status_code=404)
    except TimeoutError:
        LOGGER.debug('Timeout exceeded. Returning DEFAULT_IMAGE_URL')
        return await default_image(current_settings.DEFAULT_IMAGE_URL)


@app.route("/active/preview.png/gpu-info", methods=["GET"])
async def info_screenshot(request: 'Request') -> 'Response':
    current_settings = settings.copy()
    ip_addr = socket.gethostbyname(current_settings.CHROMIUM_HOST)
    browser_url = str(URL(scheme='http', hostname=ip_addr, port=current_settings.CHROMIUM_PORT))
    img = await EventPreviewImageGenerator.screenshot_info_page(browser_url)

    return Response(content=img, media_type="image/png")


@app.route("/health", methods=["GET"])
async def health(request: 'Request') -> 'Response':
    return PlainTextResponse('ok')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, debug=settings.DEBUG)
