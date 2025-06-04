from starlette.datastructures import URL


def cache_config(cache_url: URL, password: str = None, timeout: int = 1) -> dict:
    serializer = {'class': 'aiocache.serializers.PickleSerializer'}
    configs = {
        'memory': {
            'cache': 'aiocache.SimpleMemoryCache',
            'serializer': serializer,
            'timeout': timeout,
        },
        'redis': {
            'cache': 'aiocache.RedisCache',
            'endpoint': cache_url.hostname,
            'port': cache_url.port or 6379,
            'password': password,
            'serializer': serializer,
            'timeout': timeout,
        }
    }
    return {
        'default': configs[cache_url.scheme.lower()]
    }
