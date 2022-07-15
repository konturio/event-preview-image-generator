from starlette.datastructures import URL


def get_config(cache_url):
    cache_url = URL(cache_url)
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
            'password': None,
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
