# FastAPI Socket.IO Example

FastAPI와 Socket.IO를 결합한 실시간 통신 예제 프로젝트입니다.

## 요구사항

- Python 3.9 이상

## 설치 및 실행 방법

### 1. 가상환경 생성

```bash
python3 -m venv venv
```

### 2. 가상환경 활성화

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
python -m uvicorn main:socket_app --host 0.0.0.0 --port 8000 --reload
```

또는

```bash
python main.py
```

### 5. 서버 종료

터미널에서 `Ctrl + C`를 눌러 서버를 종료합니다.

### 6. 가상환경 비활성화

```bash
deactivate
```

## 접속 주소

- API: http://localhost:8000
- Health Check: http://localhost:8000/health
- 테스트 클라이언트: `test_client.html` 파일을 브라우저로 열기

## 프로젝트 구조

```
fastapi-socket-example/
├── app/
│   ├── api/          # REST API 라우트
│   ├── core/         # 설정 파일
│   ├── models/       # 데이터 모델
│   ├── schemas/      # Pydantic 스키마
│   ├── services/     # 비즈니스 로직
│   └── socket/       # Socket.IO 이벤트 핸들러
├── tests/            # 테스트 파일
├── main.py           # 애플리케이션 진입점
├── requirements.txt  # 의존성 목록
└── test_client.html  # Socket.IO 테스트 클라이언트
```

## 주요 기능

- FastAPI 기반 REST API
- Socket.IO를 통한 실시간 양방향 통신
- CORS 설정
- 비동기 처리 지원
