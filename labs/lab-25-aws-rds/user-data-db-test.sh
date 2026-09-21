#!/bin/bash
set -u

DB_HOST="s25-postgres.cjywss8e6e0u.ap-southeast-1.rds.amazonaws.com"
DB_PORT="5432"

exec > >(tee -a /var/log/s25-db-test.log | tee /dev/console) 2>&1

echo "=== S25 DB NETWORK TEST START ==="

for i in $(seq 1 120); do
    echo "=== S25 ATTEMPT $i ==="

    if timeout 3 bash -c "</dev/tcp/${DB_HOST}/${DB_PORT}" 2>/dev/null; then
        echo "S25_TCP_SUCCESS: RDS port 5432 reachable"
        exit 0
    else
        echo "S25_TCP_BLOCKED: RDS port 5432 not reachable"
    fi

    sleep 10
done

echo "S25_FAILED: database never became reachable"