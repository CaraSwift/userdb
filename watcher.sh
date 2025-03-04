#!/bin/bash
DB_PATH="/home/ubuntu/nvr/users.db"
PLAYBOOK_PATH="/home/ubuntu/userdb/sync_users.yml"
INVENTORY_PATH="/home/ubuntu/userdb/hosts.ini"
LOG_FILE="/var/log/db_sync.log"

echo "$(date): Starting DB watcher..." >> "$LOG_FILE"

inotifywait -m -e modify,close_write "$DB_PATH" | while read -r path action file; do
    echo "$(date): Detected change in $DB_PATH - Action: $action" >> "$LOG_FILE"
    ansible-playbook -i "$INVENTORY_PATH" "$PLAYBOOK_PATH" >> "$LOG_FILE" 2>&1
done
