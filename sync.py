# import sqlite3
# import sys

# DB_PATH = "/home/ubuntu/nvr/users.db"

# def get_passwords(db_path):
#     """Fetch passwords from the database."""
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users;")
#     users = {row[0]: (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in cursor.fetchall()}
#     print(users)
#     conn.close()
#     return users
    
# get_passwords(DB_PATH)    

import sqlite3
import sys

DB_PATH = "/home/ubuntu/nvr/users.db"

def get_passwords(db_path):
    """Fetch passwords from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, password FROM Passwords;")
    passwords = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    print(passwords)
    conn.close()
    return passwords

def update_passwords(db_path, updates):
    """Update passwords in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for name, (type_, password) in updates.items():
        cursor.execute(
            "UPDATE Passwords SET password = ? WHERE name = ? AND type = ?;",
            (password, name, type_)
        )
    conn.commit()
    conn.close()

# def main(gittest_db, local_db):
#     gittest_passwords = get_passwords(gittest_db)
#     local_passwords = get_passwords(local_db)

#     updates_needed = {
#         user: gittest_passwords[user]
#         for user in gittest_passwords
#         if user in local_passwords and gittest_passwords[user][1] != local_passwords[user][1]
#     }

#     if updates_needed:
#         update_passwords(local_db, updates_needed)
#         print(f"Updated {len(updates_needed)} passwords.")
#     else:
#         print("No password updates needed.")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python sync.py <gittest_db_path> <local_db_path>")
#         sys.exit(1)
    
#     main(sys.argv[1], sys.argv[2])
