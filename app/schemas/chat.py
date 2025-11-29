from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """채팅 메시지 스키마"""
    username: str = Field(..., min_length=1, max_length=50, description="사용자 이름")
    message: str = Field(..., min_length=1, max_length=1000, description="메시지 내용")


class ChatMessageResponse(BaseModel):
    """채팅 메시지 응답 스키마"""
    id: Optional[int] = None
    username: str
    message: str
    timestamp: str

    class Config:
        from_attributes = True


class JoinRoom(BaseModel):
    """채팅방 입장 스키마"""
    username: str = Field(..., min_length=1, max_length=50, description="사용자 이름")


class SystemMessage(BaseModel):
    """시스템 메시지 스키마"""
    type: str  # 'join', 'leave', 'info'
    message: str
    timestamp: str
