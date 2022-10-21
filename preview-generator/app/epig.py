import asyncio
import time

from pyppeteer import connect
from pyppeteer.page import Page
from pyppeteer.errors import TimeoutError
from logger import LOGGER

class EventPreviewImageGenerator(object):
    __slots__ = '_page', '_event', '_timeout', '_debug'

    def __init__(self, page: Page, timeout: int = 10000, debug: bool = False):
        self._page = page
        self._event = asyncio.Event()
        self._timeout = timeout
        self._debug = debug

    @classmethod
    async def create(cls,
                     browser_url: str,
                     width: int = 1200,
                     height: int = 630,
                     timeout: int = 10000,
                     debug: bool = False
                     ) -> 'EventPreviewImageGenerator':
        LOGGER.debug('Wait connection to browser %s', browser_url)

        browser = await connect({
            'browserURL': browser_url,
            'defaultViewport': {
                'width': width,
                'height': height
            },
            'logLevel': 'DEBUG' if debug else 'INFO'
        })

        LOGGER.debug('Wait opened tab %s', browser_url)
        page = await browser.newPage()
        instance = cls(page, timeout=timeout, debug=debug)
        LOGGER.debug('Wait exposeFunction')
        await page.exposeFunction(
            'onCustomEvent',
            instance.fire
        )
        LOGGER.debug('Connection done')

        return instance

    @staticmethod
    def _listener_func(event_name: str, debug: bool = False) -> str:
        return f'''
            () => {{
                window.addEventListener("{event_name}", ({{ type, detail }}) => {{
                    onCustomEvent();
                    {f'console.log("event fired {event_name}");' if debug else ''}
                }});
            }}
        '''

    async def listen(self, event: str) -> None:
        await self._page.evaluateOnNewDocument(self._listener_func(event, self._debug))

    async def close(self) -> None:
        await self._page.close(runBeforeUnload=False)

    async def screenshot(self, url: str, event_name: str = 'load', image_type: str = 'png') -> bytes:
        LOGGER.debug('Add listener to event %s', event_name)
        await self.listen(event_name)
        LOGGER.debug('Open page with url %s', url)
        await self._page.goto(url, {'timeout': self._timeout})
        try:
            LOGGER.debug('Wait for callback %s', url)
            await asyncio.wait_for(self._event.wait(), self._timeout / 1000)
        except asyncio.TimeoutError:
            LOGGER.debug('Exception by timeout %s', url)
            raise TimeoutError(f'Navigation Timeout Exceeded: {self._timeout} ms exceeded.')
        return await self._page.screenshot(type=image_type)

    def fire(self) -> None:
        self._event.set()

    @classmethod
    async def screenshot_info_page(cls, browser_url: str) -> bytes:
        browser = await connect({
            'browserURL': browser_url,
        })
        page = await browser.newPage()
        try:
            await page.goto('chrome://gpu')
            time.sleep(1)
            return await page.screenshot()
        finally:
            await page.close()
