from typing import TYPE_CHECKING, Optional, Dict, Any
import asyncio
import socket
import hashlib

import sentry_sdk
import ujson as json
from aiocache import caches
from aiocache.base import BaseCache
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


if settings.SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=secret.SENTRY_DSN,
        enable_tracing=True,
        environment=settings.SENTRY_ENV,
    )

app = Starlette()

if settings.CACHE_URL != '':
    caches.set_config(cache_config(settings.CACHE_URL, str(secret.CACHE_PASSWORD)))


def cache_key_context(current_settings: 'Settings') -> Dict[str, Any]:
    """Return the subset of settings that should influence cache lookups."""

    default_image_url = current_settings.DEFAULT_IMAGE_URL
    return {
        'site_url': str(current_settings.SITE_URL),
        'event_name': current_settings.EVENT_NAME,
        'image_format': current_settings.IMAGE_FORMAT,
        'width': current_settings.WIDTH,
        'height': current_settings.HEIGHT,
        'default_image_url': str(default_image_url) if default_image_url is not None else None,
    }


def cache_key_builder(f, current_settings: 'Settings') -> str:
    """Compose a deterministic key for screenshot cache entries."""

    key = {
        'module': f.__module__,
        'func': f.__name__,
        **cache_key_context(current_settings),
    }
    payload = json.dumps(key, sort_keys=True).encode('utf-8')
    return hashlib.md5(payload).hexdigest()


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
            image_type=current_settings.IMAGE_FORMAT,
            default_image=current_settings.DEFAULT_IMAGE_URL
        )
    finally:
        await epig.close()


CACHE_ALIAS = 'default'
CACHE_NAMESPACE = 'epig'
CACHE_OP_TIMEOUT_SEC = 1.0
CACHE_WRITE_TIMEOUT_SEC = 1.0


def _is_cache_enabled(current_settings: 'Settings') -> bool:
    """Return True when cache configuration should be used for the request."""

    return current_settings.CACHE_URL not in (None, '')


def _get_cache_instance() -> Optional[BaseCache]:
    """Resolve cache instance for the default alias and tolerate misconfiguration."""

    try:
        return caches.get(CACHE_ALIAS)
    except Exception:  # pragma: no cover - defensive, should rarely happen
        LOGGER.exception('Failed to resolve cache alias %s', CACHE_ALIAS)
        return None


async def get_screenshot(current_settings: 'Settings') -> bytes:
    """Return screenshot bytes while gracefully handling cache failures."""

    cache: Optional[BaseCache] = None
    cache_key: Optional[str] = None

    if _is_cache_enabled(current_settings):
        cache = _get_cache_instance()
        if cache is not None:
            cache_key = cache_key_builder(screenshot, current_settings)
            try:
                cached_value = await asyncio.wait_for(
                    cache.get(cache_key, namespace=CACHE_NAMESPACE),
                    timeout=CACHE_OP_TIMEOUT_SEC,
                )
            except asyncio.TimeoutError:
                LOGGER.exception('Timed out reading screenshot from cache', extra={'cache_key': cache_key})
            except Exception:
                LOGGER.exception('Failed to read screenshot from cache', extra={'cache_key': cache_key})
            else:
                if cached_value is not None:
                    LOGGER.debug('Cache hit for screenshot cache_key=%s', cache_key, extra={'cache_key': cache_key})
                    return cached_value

    image = await screenshot(current_settings)
    if isinstance(image, memoryview):
        image = image.tobytes()
    elif isinstance(image, bytearray):
        image = bytes(image)
    elif not isinstance(image, bytes):
        raise TypeError('Screenshot generator returned unsupported type: {0!r}'.format(type(image)))

    if cache is not None and cache_key is not None:
        try:
            await asyncio.wait_for(
                cache.set(cache_key, image, ttl=current_settings.CACHE_TTL, namespace=CACHE_NAMESPACE),
                timeout=CACHE_WRITE_TIMEOUT_SEC,
            )
            LOGGER.debug(
                'Stored screenshot in cache',
                extra={'cache_key': cache_key, 'ttl': current_settings.CACHE_TTL},
            )
        except asyncio.TimeoutError:
            LOGGER.exception('Timed out storing screenshot in cache', extra={'cache_key': cache_key})
        except Exception:
            LOGGER.exception('Failed to store screenshot in cache', extra={'cache_key': cache_key})

    return image


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

    try:
        img = await get_screenshot(current_settings)
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


def create_app():
    # sentry sdk wrapps the app into factory, so uvicorn should receive a callable
    return app

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        create_app,
        host="127.0.0.1",
        port=8000,
        factory=True,
        log_level="debug" if settings.DEBUG else "info",
    )
