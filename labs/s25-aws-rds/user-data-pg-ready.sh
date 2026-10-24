#!/bin/bash
set -euxo pipefail

DB_HOST="s25-postgres.cjywss8e6e0u.ap-southeast-1.rds.amazonaws.com"

exec > >(tee -a /var/log/s25-pg-ready.log | tee /dev/console) 2>&1

dnf install -y postgresql15

echo "=== S25 POSTGRES CHECK ==="

pg_isready \
  -h "$DB_HOST" \
  -p 5432 \
  -t 10

echo "S25_POSTGRES_READY"