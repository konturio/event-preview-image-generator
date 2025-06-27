* Remove pyppeteer
  You can use the httpx (or similar) package to call cdp endpoints directly.
* Fix or replace aiocache
  aiocache uses the old aioredis, which is now part of the redis-py package.
  aiocache has a problem with memcached
  (Improved caching logic and added invalidation and locking)
