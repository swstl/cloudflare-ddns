FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN useradd -u 10001 appuser && mkdir -p /data && chown -R appuser:appuser /data /app

RUN ln -s /data/ipv4.txt /app/ipv4.txt || true

USER appuser

VOLUME ["/data"]

CMD ["python", "-u", "/app/main.py"]

