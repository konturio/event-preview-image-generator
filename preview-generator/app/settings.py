from starlette.config import Config
from starlette.datastructures import URL, QueryParams

config = Config('../.env')

CHROMIUM_HOST = config('CHROMIUM_HOST', cast=str, default='localhost')
CHROMIUM_PORT = config('CHROMIUM_PORT', cast=int, default=9222)

USE_HEADERS = config('USE_HEADERS', cast=bool, default=False)
SITE_URL = config('SITE_URL', cast=URL, default='')
EVENT_NAME = config('EVENT_NAME', cast=str, default='load')
WIDTH = config('WIDTH', cast=int, default=1200)
HEIGHT = config('HEIGHT', cast=int, default=630)
QS = config('QS', cast=QueryParams, default='')

TIMEOUT = config('TIMEOUT', cast=int, default=10000)  # 10 seconds

CACHE_URL = config('CACHE_URL', cast=URL, default='')
CACHE_PASSWORD = config('CACHE_PASSWORD', cast=str, default=None)
CACHE_TTL = config('CACHE_TTL', cast=int, default=600)  # 10 minutes

DEBUG = config('DEBUG', cast=bool, default=False)