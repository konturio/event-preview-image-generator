from typing import TYPE_CHECKING
import logging
import socket
import ujson as json
import hashlib
from aiocache import cached, caches
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import Response
from starlette.exceptions import HTTPException
from starlette.datastructures import QueryParams, URL
from pyppeteer.errors import BrowserError, PageError
import settings
from epig import EventPreviewImageGenerator
from cache_config import cache_config

if TYPE_CHECKING:
    from starlette.requests import Request

LOGGER = logging.getLogger(__name__)

app = Starlette()

caches.set_config(cache_config(settings.CACHE_URL, settings.CACHE_PASSWORD))


def cache_key_builder(f, request: 'Request'):
    h = request.headers
    key = {
        'module': f.__module__,
        'func': f.__name__,
        'query_params': dict(request.query_params),
        'X-EPIG-url': h.get('X-EPIG-url'),
        'X-EPIG-event': h.get('X-EPIG-event'),
        'X-EPIG-width': h.get('X-EPIG-width'),
        'X-EPIG-height': h.get('X-EPIG-height'),
        'X-EPIG-qs': h.get('X-EPIG-qs')
    }
    return hashlib.md5(json.dumps(key).encode("utf-8")).hexdigest()


@app.route("/", methods=["GET"])
@cached(
    namespace="epig",
    ttl=settings.CACHE_TTL,
    alias='default',
    key_builder=cache_key_builder
)
async def preview(request: 'Request'):
    if settings.USE_HEADERS:
        h = Config(environ=request.headers)
        settings.SITE_URL = h('x-epig-url', cast=URL, default=str(settings.SITE_URL))
        settings.EVENT_NAME = h('x-epig-event', cast=str, default=settings.EVENT_NAME)
        settings.WIDTH = h('x-epig-width', cast=int, default=settings.WIDTH)
        settings.HEIGHT = h('x-epig-height', cast=int, default=settings.HEIGHT)
        settings.QS = h('x-epig-qs', cast=QueryParams, default=str(settings.QS))

    # Fix problem with DNS
    ip_addr = socket.gethostbyname(settings.CHROMIUM_HOST)

    try:
        epig = await EventPreviewImageGenerator.create(
            # str(URL(scheme='http', hostname=settings.CHROMIUM_HOST, port=settings.CHROMIUM_PORT)),
            str(URL(scheme='http', hostname=ip_addr, port=settings.CHROMIUM_PORT)),
            settings.WIDTH,
            settings.HEIGHT
        )
    except BrowserError:
        raise HTTPException(status_code=503)

    try:
        img = await epig.screenshot(
            str(
                settings.SITE_URL.include_query_params(
                    **dict(request.query_params)
                ).include_query_params(
                    **dict(settings.QS)
                )
            ),
            settings.EVENT_NAME
        )
        return Response(content=img, media_type="image/png")
    except PageError:
        raise HTTPException(status_code=404)
    finally:
        await epig.close()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, debug=settings.DEBUG)
