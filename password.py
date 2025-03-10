import sqlite3
import sys

def get_passwords(db_path):
    """Fetch passwords from the database and return as a dictionary."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute the query correctly
    cursor.execute("""
        SELECT u.name, p.type, p.password
        FROM users u
        JOIN Passwords p ON u.name = p.name
        WHERE u.can_change_own_password = 1;
    """)

    # Build the dictionary of passwords
    passwords = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    print(passwords)
    
    conn.close()
    return passwords


# def compare_users(local_users, remote_users):
#     """Compare two sets of user data and find differences."""
#     added_users = {user: data for user, data in remote_users.items() if user not in local_users}
#     removed_users = {user: data for user, data in local_users.items() if user not in remote_users}

#     modified_users = {}
#     for user in remote_users:
#         if user in local_users and remote_users[user] != local_users[user]:
#             modified_users[user] = {
#                 "old": local_users[user],
#                 "new": remote_users[user]
#             }

#     return added_users, removed_users, modified_users

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 sync.py <local_db> <remote_db>")
#         sys.exit(1)

#     local_db = sys.argv[1]
#     remote_db = sys.argv[2]

#     print(f"Comparing: Local DB = {local_db}, Remote DB = {remote_db}")

#     local_users = get_users(local_db)
#     remote_users = get_users(remote_db)

#     print(f"Local Users: {local_users}")
#     print(f"Remote Users: {remote_users}")

#     added, removed, modified = compare_users(local_users, remote_users)

#     print("\n=== Added Users ===")
#     for user, data in added.items():
#         print(f"{user}: {data}")

#     print("\n=== Removed Users ===")
#     for user, data in removed.items():
#         print(f"{user}: {data}")

#     print("\n=== Modified Users ===")
#     for user, changes in modified.items():
#         print(f"{user}: OLD {changes['old']} -> NEW {changes['new']}")
