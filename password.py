import sqlite3
import sys

#get users and passwords query
def get_users_and_passwords(db_path):
    """Fetch users and their passwords from the database where can_change_own_password = 1."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.name, p.type, p.password
        FROM users u
        JOIN passwords p ON u.name = p.name
        WHERE u.can_change_own_password = 1;
    """)

# Convert to dictionary
    users = {row[0]: {'type': row[1], 'password': row[2]} for row in cursor.fetchall()}
    conn.close()
    return users

#compare passwords for changes from remote server
def compare_users(remote_users, pc1_users):
    """Compare remote server users against gittest users and identify modifications."""
    modified_users = {}

    for user in remote_users:
        if user in pc1_users:
            if remote_users[user] != pc1_users[user]:
                modified_users[user] = {
                    "old": pc1_users[user], 
                    "new": remote_users[user]     
                }

    return modified_users


#update password on main server
def update_main_db(pc1_db, modified_users):
    """Apply password changes to the gittest database."""
    conn = sqlite3.connect(pc1_db)
    cursor = conn.cursor()

    # Modify users
    for user, changes in modified_users.items():
        cursor.execute("""
            UPDATE passwords SET 
                password = ?
            WHERE name = ? AND
            WHERE type= ?;
        """, (changes["new"]["password"], user))

    conn.commit()
    conn.close()

#defining vars 
def sync_database(pc1_db, remote_db):
    """Sync remote database with gittest database."""
    remote_users = get_users_and_passwords(remote_db)  
    pc1_users = get_users_and_passwords(pc1_db) 

    modified = compare_users(remote_users, pc1_users)

    # Print out the differences
    print(f"Remote DB = {remote_db}, PC1 DB = {pc1_db}")

    print("\n=== Modified Users ===")
    for user, changes in modified.items():
        print(f"{user}: OLD {changes['old']} -> NEW {changes['new']}")

    # Apply updates
    if modified:
        update_main_db(pc1_db, modified)
        print("Updated passwords in main database.")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sync.py <pc1_db> <remote_db>")
        sys.exit(1)

    pc1 = sys.argv[1]
    remote_db = sys.argv[2]

    sync_database(pc1, remote_db)

