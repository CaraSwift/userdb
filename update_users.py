import sqlite3

DB_PATH = "/home/ubuntu/nvr/users.db"
AXIS_DB_PATH = "/home/ubuntu/nvr/users_axis.db"  # Temporary copy from Axis

def sync_users():
    conn = sqlite3.connect(DB_PATH)
    axis_conn = sqlite3.connect(AXIS_DB_PATH)
    cur = conn.cursor()
    axis_cur = axis_conn.cursor()

    # Sync new users
    cur.execute("""
        INSERT INTO users (user_id, username, password, role)
        SELECT user_id, username, password, role FROM axis.users
        WHERE user_id NOT IN (SELECT user_id FROM users)
    """)

    # Update passwords (if changed on Omega)
    cur.execute("""
        UPDATE users
        SET password = (SELECT password FROM axis.users WHERE users.user_id = axis.users.user_id)
        WHERE users.user_id IN (SELECT user_id FROM axis.users);
    """)

    # Delete users that no longer exist on Axis
    cur.execute("DELETE FROM users WHERE user_id NOT IN (SELECT user_id FROM axis.users)")

    conn.commit()
    conn.close()
    axis_conn.close()

sync_users()
