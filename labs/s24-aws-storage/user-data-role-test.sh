#!/bin/bash
set -u

BUCKET="minh-s24-20260913153141-27072"
KEY="backups/app/hello.txt"
REGION="ap-southeast-1"

exec > >(tee -a /var/log/s24-role-test.log | tee /dev/console) 2>&1

echo "=== S24 ROLE TEST START ==="
aws --version || true

for i in $(seq 1 120); do
    echo "=== S24 ATTEMPT $i ==="
    rm -f /tmp/s24-object.txt

    if aws s3api get-object \
        --region "$REGION" \
        --bucket "$BUCKET" \
        --key "$KEY" \
        /tmp/s24-object.txt
    then
        echo "S24_SUCCESS: EC2 READ S3"
        cat /tmp/s24-object.txt
        exit 0
    else
        echo "S24_WAITING: no usable role/permission yet"
    fi

    sleep 10
done

echo "S24_FAILED: role was not available in time"