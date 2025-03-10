import sqlite3
import sys

DB_PATH = "/home/ubuntu/nvr/users.db"

def get_passwords(db_path, filter_users=False):
    """Fetch passwords from the database.
    
    If filter_users=True, only fetch users where can_change_own_password = 1.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if filter_users:
        query = """
            SELECT u.name, p.type, p.password
            FROM users u
            JOIN Passwords p ON u.name = p.name
            WHERE u.can_change_own_password = 1;
        """
    else:
        query = "SELECT name, type, password FROM Passwords;"
    
    cursor.execute(query)
    passwords = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    conn.close()
    return passwords

# def update_passwords(db_path, updates):
#     """Update passwords in the database."""
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     for name, (type_, password) in updates.items():
#         cursor.execute(
#             "UPDATE Passwords SET password = ? WHERE name = ? AND type = ?;",
#             (password, name, type_)
#         )
    
#     conn.commit()
#     conn.close()

# def main(gittest_db, local_db, is_gittest):
#     gittest_passwords = get_passwords(gittest_db, filter_users=False)
#     local_passwords = get_passwords(local_db, filter_users=not is_gittest)

#     updates_needed = {
#         user: local_passwords[user]
#         for user in local_passwords
#         if user in gittest_passwords and local_passwords[user][1] != gittest_passwords[user][1]
#     }

#     if updates_needed:
#         update_passwords(gittest_db, updates_needed)
#         print(f"Updated {len(updates_needed)} passwords on gittest.")
#     else:
#         print("No password updates needed on gittest.")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python sync_passwords.py <gittest_db_path> <local_db_path> <is_gittest>")
#         sys.exit(1)

#     gittest_db_path = sys.argv[1]
#     local_db_path = sys.argv[2]
#     is_gittest = sys.argv[3].lower() == "true"

#     main(gittest_db_path, local_db_path, is_gittest)

