from typing import Dict
from dataclasses import dataclass, fields, replace, asdict
from starlette.config import Config
from starlette.datastructures import URL, QueryParams


@dataclass
class Settings:
    CHROMIUM_HOST: str = 'localhost'
    CHROMIUM_PORT: int = 9222
    USE_HEADERS: bool = False
    SITE_URL: URL = None
    EVENT_NAME: str = 'load'
    TIMEOUT: int = 10000  # in milliseconds
    WIDTH: int = 1200  # in pixels
    HEIGHT: int = 630  # in pixels
    QS: QueryParams = ''
    ALLOW_EMPTY_QS: bool = True
    DEFAULT_IMAGE_URL: URL = None
    IMAGE_FORMAT: str = 'png'

    CACHE_URL: URL = ''
    CACHE_PASSWORD: str = None
    CACHE_TTL: int = 600  # in seconds

    DEBUG: bool = False

    def __post_init__(self):
        config = Config('../.env')
        for field in fields(self):
            value = getattr(self, field.name)
            if value == field.default:
                setattr(self, field.name, config(field.name, cast=field.type, default=field.default))
            elif not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))

    def copy(self) -> 'Settings':
        return replace(self)

    def asdict(self) -> Dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}
