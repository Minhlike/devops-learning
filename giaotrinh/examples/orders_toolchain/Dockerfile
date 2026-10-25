FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/app.py
RUN groupadd -g 10001 app && useradd -u 10001 -g app -M app \
    && mkdir /data && chown app:app /data
USER 10001:10001
ENV HOST=0.0.0.0 PORT=8080 ORDERS_DB=/data/orders.sqlite3
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/readyz',timeout=2)"
CMD ["python", "/app/app.py"]
