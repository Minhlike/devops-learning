FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --timeout 60 \
    --retries 3 \
    -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
