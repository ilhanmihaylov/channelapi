import socketio
import logging
from core.auth import *
import json


logger = logging.getLogger("tornado.general")
sio = socketio.AsyncServer(async_mode='tornado')


@sio.event
async def message(sid, message):
    await sio.emit('message', message, room=sid)


@sio.event
async def join_channel(sid, message):
    logger.debug(f"join_channel message received: {type(message)}")
    msg = json.loads(message)
    token = msg.get('token')
    auth = AuthManager()
    channel = await auth.get_channel_from_token(token)
    if not channel:
        return sio.disconnect(sid)
    sio.enter_room(sid, channel)
    await auth.token_connect(token)
    await sio.emit('clientevent', {'data': f"Connected to {channel}"}, room=sid)


@sio.event
async def connect(sid, environ):
    logger.debug(f"{sid} connected")
    sio.enter_room(sid, 'global_emit')
    await sio.emit('clientevent', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    logger.debug(f"{sid} disconnected")
