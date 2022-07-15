from typing import *
import asyncio
import uvloop
from pyppeteer import connect
from pyppeteer.page import Page


class EventPreviewImageGenerator(object):

    def __init__(self, page: Page):
        self._page = page
        self._event = asyncio.Event()

    @classmethod
    async def create(cls,
                     browser_url: str,
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
        instance = cls(page)
        await page.exposeFunction(
            'onCustomEvent',
            instance.fire
        )
        return instance

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

    async def listen(self, event: str) -> None:
        await self._page.evaluateOnNewDocument(self._listener_func(event))

    async def goto(self, url: str) -> None:
        await self._page.goto(url, {'waitUntil': 'domcontentloaded'})

    async def close(self) -> None:
        await self._page.close(runBeforeUnload=False)

    async def screenshot(self, url: str, event_name: str = 'load') -> bytes:
        await self.listen(event_name)
        await self.goto(url)
        await self._event.wait()
        data = await self._page.screenshot()
        return data

    def fire(self) -> None:
        self._event.set()
