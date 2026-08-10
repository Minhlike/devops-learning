#!/bin/bash
# 1. Nhan url tu tham so dau tien $1
URL=$1
# 2. Kiem tra neu nguoi dung khong truyen url
if [ -z "$URL" ]; then
    echo "Vui long nhap URL! vi du: ./check_endpoint.sh http://localhost"
    exit 1
fi
# 3. Chay curl lay ma http status code
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
# 4. Kiem tra xem ma http co bang 200 hay khong
if [ "$HTTP_CODE" -eq 200 ]; then
    echo "[OK] Endpoint $URL hoat dong binh thuong!"
    exit 0
else
    echo "[FAIL] Endpoint $URL bi loi! Ma HTTP: $HTTP_CODE"
    exit 1
fi
