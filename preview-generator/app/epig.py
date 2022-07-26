import asyncio
from pyppeteer import connect
from pyppeteer.page import Page


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
        browser = await connect({
            'browserURL': browser_url,
            'defaultViewport': {
                'width': width,
                'height': height
            }
        })
        page = await browser.newPage()
        instance = cls(page, timeout=timeout, debug=debug)
        await page.exposeFunction(
            'onCustomEvent',
            instance.fire
        )
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

    async def goto(self, url: str) -> None:
        await self._page.goto(url, {'waitUntil': 'domcontentloaded', 'timeout': self._timeout})

    async def close(self) -> None:
        await self._page.close(runBeforeUnload=False)

    async def screenshot(self, url: str, event_name: str = 'load', type: str = 'png') -> bytes:
        await self.listen(event_name)
        await self.goto(url)
        await self._event.wait()
        return await self._page.screenshot(type=type)

    def fire(self) -> None:
        self._event.set()
