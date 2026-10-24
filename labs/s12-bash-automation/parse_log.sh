#!/bin/bash

LOG_FILE="logs/app.log"

if [ ! -f "$LOG_FILE" ]; then
	echo "ERROR: File log $LOG_FILE khong ton tai"
	exit 1
fi

ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE")
HTTP_500_COUNT=$(grep -c "500" "$LOG_FILE")

parse_all_logs() {
    for FILE in logs/*.log; do
        ERROR_COUNT=$(grep -c "ERROR" "$FILE")
        echo "$FILE -> ERROR: $ERROR_COUNT"
    done
}

echo "Tong ERROR: $ERROR_COUNT"
echo "Tong HTTP 500: $HTTP_500_COUNT"
parse_all_logs
