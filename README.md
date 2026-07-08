## FastAPI

- fastapi, uvucorn, uv, pydatic, sqlalchemy, postgresql

- Database 구조
    - users : id, email, password, username   
    - todos : id, text, completed, created_at, author_id   
    - User와 Todo 양방향 관계 설정

- 현재 구현 상태
    - 이메일 기반 JSON 로그인
    - JWT Access Token 발급
    - 로그인 사용자 기반 Todo 작성자 저장
    - Todo 수정/삭제 권한 체크 구현

- 환경변수 설정
```
DB_URL=postgresql://[username]:[password]@localhost:5432/[db]
SECRET_KEY=
TOKEN_EXPIRE=
```

- 실행
```
1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate
// 또는 .venv\Scripts\Activate.ps1

2. 패키지 설치
uv add -r requirements.txt
// 또는 uv add pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy psycopg[binary] PyJWT pwdlib[argon2] email-validator

uv run main.py
```

- 서버 주소
http://127.0.0.1:8080

- swagger
http://127.0.0.1:8080/docs