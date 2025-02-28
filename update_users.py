import sqlite3

DB_PATH = "/home/ubuntu/nvr/users.db"
AXIS_DB_PATH = "/home/ubuntu/nvr/users_axis.db"  # Temporary copy from main server

def sync_users():
    conn = sqlite3.connect(DB_PATH)
    axis_conn = sqlite3.connect(AXIS_DB_PATH)
    cur = conn.cursor()
    axis_cur = axis_conn.cursor()

    # Sync new users
    cur.execute("""
        INSERT INTO Users (name, is_enabled, access_level, unit_group, language, remote_access, hide_inaccessible_resources, can_change_own_password, is_ldap_user, currently_in_ldap) 
        SELECT username, 1, role, 0, 0, 1, 0, 1, 0, 0
        FROM users
        WHERE username NOT IN (SELECT name FROM Users)
    """)

    # Delete users that no longer exist on Axis
    cur.execute("DELETE FROM users WHERE name NOT IN (SELECT name FROM users)")

    conn.commit()
    conn.close()
    axis_conn.close()

sync_users()
