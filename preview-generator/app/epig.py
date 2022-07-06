from typing import *
import asyncio
import uvloop
from pyppeteer import connect
from pyppeteer.page import Page


class EventPreviewImageGenerator(object):
    event = asyncio.Event()

    def __init__(self, page: Page):
        self._page = page

    @classmethod
    async def create(cls,
                     browser_url: str = 'http://chromium-headless:9222',
                     width: int = 1200,
                     height: int = 630
                     ) -> 'EventPreviewImageGenerator':
        browser = await connect({
            'browserURL': browser_url,
            'defaultViewport': {
                'width': width,
                'height': height
            }
        })
        page = await browser.newPage()
        await page.exposeFunction(
            'onCustomEvent',
            cls.fire
        )
        return cls(page)

    @staticmethod
    def _listener_func(event_name: str) -> str:
        return f'''
            () => {{
                window.addEventListener("{event_name}", ({{ type, detail }}) => {{
                    onCustomEvent();
                    <!-- console.log('event fired {event_name}'); -->
                }});
            }}
        '''

    @classmethod
    def fire(cls) -> None:
        cls.event.set()

    async def listen(self, event: str) -> None:
        await self._page.evaluateOnNewDocument(self._listener_func(event))

    async def goto(self, url: str) -> None:
        await self._page.goto(url, {'waitUntil': 'networkidle0'})

    async def close(self) -> None:
        await self._page.close()

    async def screenshot(self, url: str, event_name: str = 'load') -> bytes:
        await self.listen(event_name)
        await self.goto(url)
        await self.event.wait()
        data = await self._page.screenshot()
        return data
