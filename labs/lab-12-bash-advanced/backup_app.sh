#!/bin/bash

SOURCE_DIR="app"
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/app-$TIMESTAMP.tar.gz"

check_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "ERROR: Thu muc $BACKUP_DIR khong ton tai"
        return 1
    fi

    echo "OK: Thu muc $BACKUP_DIR ton tai"
    return 0
}

backup_app() {
    if [ ! -d "$SOURCE_DIR" ]; then
        echo "ERROR: Thu muc $SOURCE_DIR khong ton tai"
        return 1
    fi

    if tar -czf "$BACKUP_FILE" "$SOURCE_DIR/"; then
        echo "Backup thanh cong: $BACKUP_FILE"
        return 0
    else
        echo "ERROR: Backup that bai"
        return 1
    fi
}

if check_backup_dir; then
    backup_app
else
    echo "Dung script vi thu muc backup khong hop le"
    exit 1
fi


