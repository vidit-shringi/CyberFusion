FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY simulator ./simulator
COPY datasets ./datasets
COPY docs ./docs

RUN useradd --create-home --shell /usr/sbin/nologin cyberfusion \
    && chown -R cyberfusion:cyberfusion /app
USER cyberfusion

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
