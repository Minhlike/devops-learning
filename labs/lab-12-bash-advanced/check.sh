#!/bin/bash
BACKUP_DIR="backups"
check_backup_dir() {

    if [ ! -d "$BACKUP_DIR" ]; then
        echo "ERROR: Thu muc $BACKUP_DIR khong ton tai"
        return 1
    fi

    echo "OK: Thu muc $BACKUP_DIR ton tai"
    return 0
}
