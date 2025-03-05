#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import sqlite3
import hashlib
import os

def get_users_and_passwords(db_path):
    """Retrieve users who can change their password along with their password hashes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.name, p.password
        FROM users u
        JOIN Passwords p ON u.name = p.name
        WHERE u.can_change_own_password = 1
    """)
    users = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return users

def sync_passwords(source_db, target_db):
    """Compare passwords and update if necessary."""
    source_data = get_users_and_passwords(source_db)
    target_data = get_users_and_passwords(target_db)

    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()

    updates = 0
    for user, password in source_data.items():
        if user not in target_data or target_data[user] != password:
            cursor.execute("""
                INSERT INTO Passwords (name, password)
                VALUES (?, ?)
                ON CONFLICT(name) DO UPDATE SET password=excluded.password
            """, (user, password))
            updates += 1

    conn.commit()
    conn.close()

    return updates

def main():
    module_args = dict(
        source_db=dict(type="str", required=True),
        target_db=dict(type="str", required=True)
    )

    module = AnsibleModule(argument_spec=module_args)

    source_db = module.params["source_db"]
    target_db = module.params["target_db"]

    updates = sync_passwords(source_db, target_db)

    module.exit_json(changed=updates > 0, msg=f"{updates} passwords synchronized.")

if __name__ == "__main__":
    main()


