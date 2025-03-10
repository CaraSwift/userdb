import sqlite3
import sys

DB_PATH = "/home/ubuntu/nvr/users.db"

def get_passwords(db_path):
    """Fetch passwords from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, password FROM Passwords;")
    passwords = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    conn.close()
    return passwords