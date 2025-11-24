from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 앱 기본 설정
    APP_NAME: str = "FastAPI Socket.IO Test"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS 설정
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Socket.IO 설정
    SOCKETIO_CORS_ALLOWED_ORIGINS: str = "*"
    SOCKETIO_ASYNC_MODE: str = "asgi"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
