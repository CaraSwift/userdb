#!/bin/bash
DB_PATH="/home/ubuntu/nvr/users.db"
PLAYBOOK_PATH="/home/ubuntu/userdb/sync_users.yml"
INVENTORY_PATH="/home/ubuntu/userdb/hosts.ini"

inotifywait -m -e modify,close_write $DB_PATH | while read path action file; do
    echo "Detected change in $DB_PATH. Running Ansible..."
    ansible-playbook -i $INVENTORY_PATH $PLAYBOOK_PATH
done
