FROM python:3.12-slim

WORKDIR /app

# Install package sistem dan font standar
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL="sqlite:////app/storage/arsitex.db"
ENV STORAGE_DIR="/app/storage"
ENV PYTHONPATH=/app

RUN mkdir -p /app/storage

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

