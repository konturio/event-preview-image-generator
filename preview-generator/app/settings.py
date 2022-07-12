from starlette.config import Config
from starlette.datastructures import URLPath, URL, QueryParams

config = Config("../.env")

USE_HEADERS = config("USE_HEADERS", cast=bool, default=False)
SITE_URL = config("SITE_URL", cast=URL, default=None)
CDP_HOST = config("CDP_HOST", cast=str, default='localhost')
CDP_PORT = config("CDP_PORT", cast=int, default=9222)
EVENT_NAME = config("EVENT_NAME", cast=str, default='load')
WIDTH = config("WIDTH", cast=int, default=1200)
HEIGHT = config("HEIGHT", cast=int, default=630)
QS = config("QS", cast=QueryParams, default="")
