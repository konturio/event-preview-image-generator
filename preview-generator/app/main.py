import os
from typing import TYPE_CHECKING
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.datastructures import QueryParams, URL
import settings
from epig import EventPreviewImageGenerator
from starlette.config import Config
import socket
from caches import Cache
from asgi_caches.middleware import CacheMiddleware

if TYPE_CHECKING:
    from starlette.requests import Request

app = Starlette()

cache = Cache("locmem://null", key_prefix="epig", ttl=os.environ.get('TTL', 60 * 60))
app.add_event_handler("startup", cache.connect)
app.add_event_handler("shutdown", cache.disconnect)

app.add_middleware(CacheMiddleware, cache=cache)


@app.route("/", methods=["GET"])
async def preview(request: 'Request'):
    if settings.USE_HEADERS:
        h = Config(environ=request.headers)
        settings.SITE_URL = h('x-epig-url', cast=URL, default=str(settings.SITE_URL))
        settings.EVENT_NAME = h('x-epig-event', cast=str, default=settings.EVENT_NAME)
        settings.WIDTH = h('x-epig-width', cast=int, default=settings.WIDTH)
        settings.HEIGHT = h('x-epig-height', cast=int, default=settings.HEIGHT)
        settings.QS = h('x-epig-qs', cast=QueryParams, default=str(settings.QS))

    # TODO: try if CDP_HOST not exists
    # Fix problem with DNS
    ip_addr = socket.gethostbyname(settings.CDP_HOST)

    epig = await EventPreviewImageGenerator.create(
        # str(URL(scheme='http', hostname=settings.CDP_HOST, port=settings.CDP_PORT)),
        str(URL(scheme='http', hostname=ip_addr, port=settings.CDP_PORT)),
        settings.WIDTH,
        settings.HEIGHT
    )
    # TODO: try if site_url not exists
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
    await epig.close()

    return Response(content=img, media_type="image/png")
