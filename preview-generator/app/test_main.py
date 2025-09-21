import pytest
from starlette.datastructures import URL
from unittest.mock import AsyncMock, Mock

import main


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    """Limit anyio tests to asyncio backend to avoid extra dependencies."""

    return 'asyncio'


async def test_get_screenshot_returns_cached_value(monkeypatch):
    """Ensure cached bytes are returned without invoking the generator."""

    cached_bytes = b'cached-image'
    settings = main.Settings(CACHE_URL=URL('redis://cache'), CACHE_TTL=10)

    cache_mock = Mock()
    cache_mock.get = AsyncMock(return_value=cached_bytes)
    cache_mock.set = AsyncMock()
    monkeypatch.setattr(main, 'caches', Mock(get=Mock(return_value=cache_mock)))
    monkeypatch.setattr(main, 'screenshot', AsyncMock())

    result = await main.get_screenshot(settings)

    assert result == cached_bytes, 'expected cached screenshot bytes to be returned'
    assert cache_mock.get.await_count == 1, 'expected cache.get to be awaited exactly once on cache hit'
    assert not main.screenshot.await_args_list, 'expected screenshot generator to be skipped on cache hit'
    assert cache_mock.set.await_count == 0, 'expected cache.set not to be awaited on cache hit'


async def test_get_screenshot_fallbacks_when_cache_fails(monkeypatch):
    """When cache errors occur the screenshot should still be generated."""

    generated_bytes = b'generated-image'
    settings = main.Settings(CACHE_URL=URL('redis://cache'), CACHE_TTL=10)

    cache_mock = Mock()
    cache_mock.get = AsyncMock(side_effect=TypeError('boom'))
    cache_mock.set = AsyncMock(side_effect=TypeError('boom'))
    monkeypatch.setattr(main, 'caches', Mock(get=Mock(return_value=cache_mock)))
    monkeypatch.setattr(main, 'screenshot', AsyncMock(return_value=generated_bytes))

    result = await main.get_screenshot(settings)

    assert result == generated_bytes, 'expected screenshot generation fallback when cache fails'
    assert cache_mock.get.await_count == 1, 'expected cache.get to be awaited exactly once despite read failure'
    assert main.screenshot.await_count == 1, 'expected screenshot generator to run exactly once'
    assert cache_mock.set.await_count == 1, 'expected cache.set to be awaited exactly once despite failure'


async def test_get_screenshot_without_cache(monkeypatch):
    """The generator should run when caching is disabled."""

    generated_bytes = b'generated-image'
    settings = main.Settings()

    monkeypatch.setattr(main, 'screenshot', AsyncMock(return_value=generated_bytes))

    result = await main.get_screenshot(settings)

    assert result == generated_bytes, 'expected screenshot bytes when cache disabled'
    assert main.screenshot.await_count == 1, 'expected screenshot generator to run when cache disabled'
