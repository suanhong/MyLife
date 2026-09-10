FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV PORT=8080
CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 app:app
