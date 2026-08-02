#!/bin/bash
echo "=== $(date) ===" >> /mnt/d/Devops/linux-labs/lab-05-resources/disk_audit.log
df -h /mnt/d >> /mnt/d/Devops/linux-labs/lab-05-resources/disk_audit.log
