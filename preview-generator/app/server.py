import os
import socket
import logging
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from aiohttp import web
from epig import EventPreviewImageGenerator

LOGGER = logging.getLogger(__name__)


# TODO: move to debug
async def index_handler(request: web.Request):
    link = 'localhost:8080'
    body = f"""
        <html prefix="og: http://ogp.me/ns#">
        <head>
            <!-- HTML Meta Tags -->
            <title>Event Preview Image Generator</title>
            <meta name="description" content="Event Preview Image Generator">
            
            <!-- Facebook Meta Tags -->
            <meta property="og:url" content="{link}">
            <meta property="og:type" content="website">
            <meta property="og:title" content="Event Preview Image Generator">
            <meta property="og:description" content="Event Preview Image Generator">
            <meta property="og:image" content="{link}/preview.png">
            <meta property="og:image:width" content="1200"/>
            <meta property="og:image:height" content="630"/>
            
            <!-- Twitter Meta Tags -->
            <meta name="twitter:card" content="summary_large_image">
            <meta property="twitter:domain" content="event-preview-image-generator.loca.lt">
            <meta property="twitter:url" content="{link}">
            <meta name="twitter:title" content="Event Preview Image Generator">
            <meta name="twitter:description" content="Event Preview Image Generator">
            <meta name="twitter:image" content="{link}/preview.png">
            
            <!-- Meta Tags Generated via https://www.opengraph.xyz -->   
        </head>
        <body>
        </body>
        </html>
    """
    return web.Response(text=body, content_type='text/html')


@dataclass
class Environ:
    SITE_URL: str
    CDP_HOST: str
    CDP_PORT: str = '9222'
    EVENT_NAME: str = 'load'
    WIDTH: int = 1200
    HEIGHT: int = 630
    ADDITIONAL_QUERY_STRING: str = ''


async def screenshot_handler(request: web.Request):
    # TODO: use Environ dataclass
    # env = Environ(**request.app['environ'])
    event_name = request.app['environ'].get('EVENT_NAME', 'load')
    width = int(request.app['environ'].get('WIDTH', '1200'))
    height = int(request.app['environ'].get('HEIGHT', '630'))
    cdp_host = request.app['environ']['CDP_HOST']
    cdp_port = request.app['environ'].get('CDP_PORT', '9222')
    additional_query_string = request.app['environ'].get('ADDITIONAL_QUERY_STRING', '')
    site_url = request.app['environ']['SITE_URL']

    # Fix problem with DNS
    ip_addr = socket.gethostbyname(cdp_host)

    # Inject qs_additional
    if len(additional_query_string):
        url_parts = list(urlparse(site_url))
        query_dict = parse_qs(url_parts[4])
        query_dict.update(parse_qs(additional_query_string))
        url_parts[4] = urlencode(query_dict, doseq=True)
        site_url = urlunparse(url_parts)

    e = await EventPreviewImageGenerator.create(f'http://{ip_addr}:{cdp_port}', width, height)
    img = await e.screenshot(site_url, event_name)
    await e.close()
    return web.Response(body=img, content_type="image/png")


def setup_routes(app):
    app.add_routes([
        # TODO: move root route to debug
        web.get('/', index_handler),
        web.get('/preview.{format}', screenshot_handler),
    ])


async def shutdown():
    pass


async def web_app():
    logging.basicConfig(level=logging.INFO)
    LOGGER.info("Server Starting")
    app = web.Application()
    app['environ'] = os.environ
    setup_routes(app)
    app.on_shutdown.append(shutdown)
    return app
