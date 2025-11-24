from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.core.config import settings
from app.socket.events import register_socket_events
from app.api.routes.main import router as main_router

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# API 라우터 등록
app.include_router(main_router, tags=["main"])

# Socket.IO 서버 생성
sio = socketio.AsyncServer(
    async_mode=settings.SOCKETIO_ASYNC_MODE,
    cors_allowed_origins=settings.SOCKETIO_CORS_ALLOWED_ORIGINS
)

# Socket.IO 이벤트 핸들러 등록
register_socket_events(sio)

# Socket.IO 앱을 FastAPI와 결합
socket_app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host=settings.HOST, port=settings.PORT)
