import sqlite3
import sys

def get_users_and_passwords(db_path):
    """Fetch users and their passwords from the database where can_change_own_password = 1."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the query to fetch users with passwords
    cursor.execute("""
        SELECT u.name, p.type, p.password
        FROM users u
        JOIN Passwords p ON u.name = p.name
        WHERE u.can_change_own_password = 1;
    """)

    # Convert the result into a dictionary
    users = {row[0]: {'type': row[1], 'password': row[2]} for row in cursor.fetchall()}
    conn.close()
    return users

def compare_users(local_users, remote_users):
    """Compare two sets of user data and find differences, with the assumption that local data is new."""
    added_users = {user: data for user, data in local_users.items() if user not in remote_users}
    removed_users = {user: data for user, data in remote_users.items() if user not in local_users}

    modified_users = {}
    for user in local_users:
        if user in remote_users:
            if local_users[user] != remote_users[user]:
                modified_users[user] = {
                    "old": remote_users[user], 
                    "new": local_users[user]    
                }

    return added_users, removed_users, modified_users



def sync_database(gittest_db, remote_db):
    """Sync remote database with gittest database."""
    local_users = get_users_and_passwords(remote_db)
    remote_users = get_users_and_passwords(gittest_db)

    added, removed, modified = compare_users(local_users, remote_users)

    # Print out the differences
    print(f"Local DB = {remote_db}, Gittest DB = {gittest_db}")

    print("\n=== Added Users ===")
    for user, data in added.items():
        print(f"{user}: {data}")

    print("\n=== Removed Users ===")
    for user, data in removed.items():
        print(f"{user}: {data}")

    print("\n=== Modified Users ===")
    for user, changes in modified.items():
        print(f"{user}: OLD {changes['old']} -> NEW {changes['new']}")

    # Here you can add logic to implement the changes in the gittest database if needed
    # For example: adding missing users or updating passwords, etc.

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sync.py <gittest_db> <remote_db>")
        sys.exit(1)

    gittest_db = sys.argv[1]
    remote_db = sys.argv[2]

    sync_database(gittest_db, remote_db)
