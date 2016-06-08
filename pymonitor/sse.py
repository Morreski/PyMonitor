from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado.iostream import StreamClosedError
import aiopg
import asyncio
import psutil
import json


class SSEResponse:

    def __init__(self, data, message_id=None, is_comment=False):
        self.data = str(data)
        self.message_id = message_id
        self.is_comment = is_comment

    def __str__(self):
        if self.is_comment:
            return ": %s" % self.data
        s = "".join(["data: " + ss for ss in self.data.split("\n")])

        if self.message_id is not None:
            s += "\nid: %s" % self.message_id

        s += "\n\n"
        return s


class DataSource:

    def __init__(self, max_iterations=1, forever=False):
        self.max_iterations = max_iterations
        self.forever = forever
        self.current_iteration = 0

    async def __aiter__(self):
        return self

    async def __anext__(self):
        self.current_iteration += 1
        if self.current_iteration <= self.max_iterations or self.forever:
            yielded = await self.loop()
            return yielded
        raise StopAsyncIteration

    async def loop(self):
        raise NotImplementedError


class SSEDataSource(DataSource):

    async def loop(self):
        message = psutil.cpu_percent(percpu=True)
        await asyncio.sleep(1)
        return json.dumps(message)


class DiskDataSource(DataSource):

    async def loop(self):
        partitions = [p.mountpoint for p in psutil.disk_partitions()]
        percents = {p: psutil.disk_usage(p).percent for p in partitions}
        await asyncio.sleep(1)
        return json.dumps(percents)


class AsyncioSSEHandler(RequestHandler):

    def initialize(self, datasource):
        self.datasource = datasource
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache/no-store')

    async def publish(self, response):
        self.write(str(response))
        self.flush()

    async def get(self, *args, **kwargs):
        datasource = self.datasource(forever=True)
        async for data in datasource:
            await self.publish(SSEResponse(data))
