import socketio


def register_socket_events(sio: socketio.AsyncServer):
    """Socket.IO 이벤트 핸들러 등록"""

    @sio.event
    async def connect(sid, environ):
        """클라이언트 연결 이벤트"""
        print(f"Client connected: {sid}")
        await sio.emit('message', {'data': 'Connected to server'}, room=sid)

    @sio.event
    async def disconnect(sid):
        """클라이언트 연결 해제 이벤트"""
        print(f"Client disconnected: {sid}")

    @sio.event
    async def message(sid, data):
        """메시지 수신 이벤트"""
        print(f"Message from {sid}: {data}")
        await sio.emit('response', {'data': f'Server received: {data}'}, room=sid)

    return sio
