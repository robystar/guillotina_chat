from guillotina.async_util import IAsyncUtility
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.utils import get_authenticated_user_id, get_current_request

import asyncio
import orjson
import logging

logger = logging.getLogger('guillotina_chat')

class IMessageSender(IAsyncUtility):
    pass

class MessageSenderUtility:
    def __init__(self, settings=None, loop=None):
        self._loop = loop
        self._settings = {}
        self._webservices = []
        self._closed = False

    def register_ws(self, ws, request):
        ws.user_id = get_authenticated_user_id()
        self._webservices.append(ws)

    def unregister_ws(self, ws):
        self._webservices.remove(ws)

    async def send_message(self, message):
        summary = await get_multi_adapter(
            (message, get_current_request()),
            IResourceSerializeToJsonSummary)()
        await self._queue.put((message, summary))

    async def finalize(self):
        self._closed = True

    async def initialize(self, app=None):
        self._queue = asyncio.Queue()

        while not self._closed:
            try:
                message, summary = await asyncio.wait_for(self._queue.get(), 0.2)
                for user_id in message.__parent__.users:
                    for ws in self._webservices:
                        if ws.user_id == user_id:
                            await ws.send_str(orjson.dumps(summary))
            except (RuntimeError, asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception:
                logger.warning(
                    'Error sending message',
                    exc_info=True)
                await asyncio.sleep(1)
