import sqlite3
import sys

DB_PATH = "/home/ubuntu/nvr/users.db"

def get_passwords(db_path):
    """Fetch passwords from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = {row[0]: (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in cursor.fetchall()}
    conn.close()
    return users
    
get_passwords(DB_PATH)    