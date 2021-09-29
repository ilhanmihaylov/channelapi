import tornado
from core.auth import *
from core import websocket
from tornado.web import authenticated

class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        auth = self.request.headers.get('Authorization', None)

        if auth == options.auth_key:
            self.current_user = 1

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class ChannelHandler(BaseHandler):

    @authenticated
    async def post(self, channel):
        if not channel:
            error_message = dict(success=False, message="No Channel Supplied")
            return self.finish(error_message)

        auth = AuthManager()
        token = await auth.create_or_get_channel_token(channel)
        self.write(dict(success=True, token=token))


"""    async def get(self, channel):
        if not channel:
            error_message = dict(success=False, message="No Channel Supplied")
            return self.finish(error_message)
        
        auth = AuthManager()
        channel_info = await auth.describe_channel(channel)
        if not channel_info:
            error_message = dict(success=False, message="Channel Does Not Exist")
            return self.finish(error_message)
        self.write(channel_info)"""


class MessageHandler(BaseHandler):
    @authenticated
    async def post(self, channel):
        if not channel:
            error_message = dict(success=False, message="No Channel Supplied")
            return self.finish(error_message)

        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            self.write(dict(success=False, message="Body is in incorrect format. Key 'message' not found."))
            self.finish()

        await websocket.sio.emit("message", data.get('message'), room=channel)
        self.write({"success": True})
    