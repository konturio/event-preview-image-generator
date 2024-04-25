import logging
from datetime import datetime

from settings import Settings

import ujson as json


class JsonFormatter(logging.Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "timestamp": datetime.utcfromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "message": record.getMessage(),
            "logger": record.name,
        })

settings = Settings()
LOGGER = logging.root
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
LOGGER.handlers = [handler]
LOGGER.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
