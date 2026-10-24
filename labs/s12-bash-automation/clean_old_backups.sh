#!/bin/bash

BACKUP_DIR="backups"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "ERROR: Thu muc $BACKUP_DIR khong ton tai"
    exit 1
fi

if [ "$BACKUP_DIR" != "backups" ]; then
    echo "ERROR: Duong dan backup khong an toan: $BACKUP_DIR"
    exit 1
fi

echo "Cac backup cu hon 7 ngay:"

find "$BACKUP_DIR" \
    -type f \
    -name "*.tar.gz" \
    -mtime +7 \
    -print \
    -delete

echo "Cleanup hoan thanh"

