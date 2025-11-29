import socketio
from datetime import datetime
from app.core.database import db

# 연결된 사용자 정보 저장 (sid -> username)
connected_users = {}


def register_socket_events(sio: socketio.AsyncServer):
    """Socket.IO 이벤트 핸들러 등록"""

    @sio.event
    async def connect(sid, environ):
        """클라이언트 연결 이벤트"""
        print(f"Client connected: {sid}")
        await sio.emit('connected', {'session_id': sid}, room=sid)

    @sio.event
    async def disconnect(sid):
        """클라이언트 연결 해제 이벤트"""
        print(f"Client disconnected: {sid}")

        # 사용자가 채팅방에 입장했었다면 퇴장 알림
        if sid in connected_users:
            username = connected_users[sid]
            del connected_users[sid]

            # 모든 클라이언트에게 퇴장 알림
            await sio.emit('user_left', {
                'username': username,
                'message': f'{username}님이 퇴장했습니다',
                'timestamp': datetime.now().isoformat(),
                'online_users': len(connected_users)
            })

    @sio.event
    async def join_chat(sid, data):
        """채팅방 입장 이벤트"""
        username = data.get('username', f'User_{sid[:8]}')

        # 사용자 정보 저장
        connected_users[sid] = username

        print(f"{username} joined the chat (sid: {sid})")

        # 최근 메시지 히스토리 전송 (본인에게만)
        recent_messages = db.get_recent_messages(limit=50)
        await sio.emit('message_history', {
            'messages': recent_messages
        }, room=sid)

        # 모든 클라이언트에게 입장 알림
        await sio.emit('user_joined', {
            'username': username,
            'message': f'{username}님이 입장했습니다',
            'timestamp': datetime.now().isoformat(),
            'online_users': len(connected_users)
        })

    @sio.event
    async def send_message(sid, data):
        """메시지 전송 이벤트"""
        # 사용자가 채팅방에 입장했는지 확인
        if sid not in connected_users:
            await sio.emit('error', {
                'message': '먼저 채팅방에 입장해주세요'
            }, room=sid)
            return

        username = connected_users[sid]
        message_text = data.get('message', '')

        if not message_text.strip():
            return

        print(f"Message from {username}: {message_text}")

        # 데이터베이스에 메시지 저장
        saved_message = db.save_message(username, message_text)

        # 모든 클라이언트에게 메시지 브로드캐스트
        await sio.emit('new_message', {
            'id': saved_message['id'],
            'username': saved_message['username'],
            'message': saved_message['message'],
            'timestamp': saved_message['timestamp']
        })

    @sio.event
    async def get_online_users(sid, data):
        """온라인 사용자 목록 요청"""
        await sio.emit('online_users', {
            'count': len(connected_users),
            'users': list(connected_users.values())
        }, room=sid)

    return sio
