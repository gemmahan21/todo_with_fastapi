## FastAPI

- fastapi, uvucorn, uv, pydatic, sqlalchemy, postgresql

- 환경변수 설정
```
DB_URL=postgresql://[username]:[password]@localhost:5432/[db]
SECRET_KEY=
TOKEN_EXPIRE=
```

- 프로젝트 구조
todo/
├─ main.py
├─ .env
├─ .gitignore
├─ requirements.txt
└─ app/
   ├─ __init__.py
   ├─ main.py
   ├─ config.py
   ├─ database.py
   ├─ models.py
   ├─ schemas.py
   ├─ helpers.py
   └─ security.py

- 실행
```
source .venv/bin/activate
uv run main.py
```

- swagger
http://127.0.0.1:8080/docs