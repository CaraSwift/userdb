import sqlite3

DB_PATH = "/home/ubuntu/nvr/users.db"
AXIS_DB_PATH = "/home/ubuntu/nvr/users_axis.db"  # Temp copy from main server

def sync_users():
    conn = sqlite3.connect(DB_PATH)
    axis_conn = sqlite3.connect(AXIS_DB_PATH)
    cur = conn.cursor()
    axis_cur = axis_conn.cursor()

    # Add new users
    cur.execute("""
        INSERT INTO Users (name, is_enabled, access_level, unit_group, language, remote_access, hide_inaccessible_resources, can_change_own_password, is_ldap_user, currently_in_ldap) 
        SELECT name, 1, 0, 0, 0, 1, 0, 1, 0, 0
        FROM users
        WHERE name NOT IN (SELECT name FROM Users)
    """)

    # Update modified users
    cur.execute("""
        UPDATE Users
        SET is_enabled = 1, access_level = 0, unit_group = 0, language = 0, remote_access = 1, hide_inaccessible_resources = 0, can_change_own_password = 1, is_ldap_user = 0, currently_in_ldap = 0
        WHERE name IN (SELECT name FROM users WHERE Users.is_enabled != 1 OR Users.access_level != 0)
    """)

    # Sync deleted users
    cur.execute("""
        DELETE FROM Users
        WHERE name NOT IN (SELECT name FROM users)
    """)

    conn.commit()
    conn.close()
    axis_conn.close()

sync_users()
