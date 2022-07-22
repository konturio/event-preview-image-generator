from starlette.datastructures import URL


def cache_config(cache_url: URL, password: str = None) -> dict:
    serializer = {'class': 'aiocache.serializers.PickleSerializer'}
    configs = {
        'default': {
            'cache': 'aiocache.SimpleMemoryCache',
            'serializer': serializer
        },
        'redis': {
            'cache': 'aiocache.RedisCache',
            'endpoint': cache_url.hostname,
            'port': cache_url.port or 6379,
            'password': password,
            'serializer': serializer
        },
        'memcached': {
            'cache': 'aiocache.MemcachedCache',
            'endpoint': cache_url.hostname,
            'port': cache_url.port or 11211,
            'serializer': serializer
        }
    }
    return {
        'default': configs[cache_url.scheme.lower() or 'default']
    }
