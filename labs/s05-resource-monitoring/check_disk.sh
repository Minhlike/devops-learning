#!/bin/bash
LOG_FILE="$(dirname "$0")/disk_audit.log"
echo "=== $(date) ===" >> "$LOG_FILE"
df -h /mnt/d >> "$LOG_FILE"
