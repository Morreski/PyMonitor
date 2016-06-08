from tornado import web, ioloop
from tornado.options import options, define
import tornado

from sse import AsyncioSSEHandler, SSEDataSource, DiskDataSource
import asyncio

define("port", default="1337", help="The server port")

define("static_path", default="../website", help="Static file location (root)")


def make_app():
    routes = [
        (r"^/api/cpu$", AsyncioSSEHandler, {'datasource': SSEDataSource}),
        (r"^/api/disks$", AsyncioSSEHandler, {'datasource': DiskDataSource}),
        (r"^/(.*)$", web.StaticFileHandler, {'path': options.static_path, "default_filename": "index.html"}),
    ]
    return web.Application(
        routes,
        static_path=options.static_path,
        debug=True
    )

if __name__ == '__main__':
    options.parse_command_line()
    tornado.platform.asyncio.AsyncIOMainLoop().install()  # Use asyncio event loop instead of tornado ioloop.
    app = make_app()
    app.listen(options.port)
    asyncio.get_event_loop().run_forever()
