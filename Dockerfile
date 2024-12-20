FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install poetry && poetry config virtualenvs.create false
COPY / /app/
RUN poetry install --no-interaction --no-ansi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
