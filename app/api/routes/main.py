from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "FastAPI Socket.IO Server is running"}


@router.get("/health")
async def health():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
