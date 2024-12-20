from os import environ

import uvicorn
from app import app

# Для разработки из-под виртуального окружения или запуска локально.
if __name__ == "__main__":
    host = environ.get("HOST", "localhost")
    port = int(environ.get("PORT", 8002))
    uvicorn.run(app="main:app", host=host, port=port, reload=True)
