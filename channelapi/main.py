import tornado.ioloop
import tornado.web
import logging
import socketio
from tornado.options import define, options
from core import websocket
from core.rest import rest

logger = logging.getLogger("tornado.general")

define("debug", default=False, type=bool, help="Start in debug mode")
define("redis_host", default="localhost", type=bool, help="Auth Redis Hostname")
define("redis_port", default=6379, type=bool, help="Auth Redis Port")
define("port", default=8888, type=bool, help="Server port")
define("auth_key", default="s3cur3_t0k3n", type=str, help="Authorization token for rest requests")


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        await websocket.sio.emit("clientevent", "test12345", room='global_emit')
        self.write("Hello, world")


tornado.options.parse_command_line()

def make_app():
    if options.debug:
        logger.setLevel(logging.DEBUG)

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/socket.io/", socketio.get_tornado_handler(websocket.sio)),
        (r"/channel/(.*)", rest.ChannelHandler),
        (r"/message/(.*)", rest.MessageHandler),

    ], debug=options.debug, autoreload=options.debug)


if __name__ == "__main__":
    app = make_app()
    app.listen(options.port)
    logger.debug(f"Starting... Port: {options.port} Tornado Version: {tornado.version} ")
    if options.debug:
        logger.debug("Debug mode enabled.")
    tornado.ioloop.IOLoop.current().start()