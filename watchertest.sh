#!/bin/bash
DB_PATH="/usr/nvr/unitconfig/db/users.db"
LOG_FILE="/var/log/db_sync.log"

echo "$(date): Starting DB watcher..." >> "$LOG_FILE"

inotifywait -m -e modify,close_write "$DB_PATH" | while read -r path action file; do
    echo "$(date): Detected change in $DB_PATH - Action: $action" >> "$LOG_FILE"
done
