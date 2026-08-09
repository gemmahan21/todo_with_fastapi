import uvicorn
from app.config import get_settings

settings = get_settings()


def main():
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)


if __name__ == "__main__":
    main()
