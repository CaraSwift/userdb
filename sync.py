import sqlite3
import sys

def get_users(db_path):
    """Fetch users from the database and return as a dictionary."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = {row[0]: tuple(map(int, row[1:])) for row in cursor.fetchall()}
    conn.close()
    return users

def get_passwords(db_path):
    """Fetch passwords from the database and return as a dictionary."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, password FROM passwords;")
    passwords = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    conn.close()
    return passwords

def compare_users(local_users, remote_users):
    """Compare two sets of user data and find differences."""
    added_users = {user: data for user, data in remote_users.items() if user not in local_users}
    removed_users = {user: data for user, data in local_users.items() if user not in remote_users}

    modified_users = {}
    for user in remote_users:
        if user in local_users and remote_users[user] != local_users[user]:
            modified_users[user] = {
                "old": local_users[user],
                "new": remote_users[user]
            }

    return added_users, removed_users, modified_users

def update_remote_db(remote_db, added_users, removed_users, modified_users, local_passwords):
    """Apply changes to the remote database, including inserting passwords for new users."""
    conn = sqlite3.connect(remote_db)
    cursor = conn.cursor()

    # Add new users
    for user, data in added_users.items():
        cursor.execute("SELECT COUNT(*) FROM users WHERE name = ?", (user,))
        if cursor.fetchone()[0] == 0:  # User does not exist
            try:
                cursor.execute("""
                    INSERT INTO users (name, is_enabled, access_level, unit_group, language, remote_access, 
                                    hide_inaccessible_resources, can_change_own_password, is_ldap_user, 
                                    currently_in_ldap)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user, *data))

                # Check if there's a password for this new user and insert it
                if user in local_passwords:
                    # Unpack the (type, password) tuple
                    user_type, user_password = local_passwords[user]
                    cursor.execute("""
                        INSERT INTO passwords (name, type, password)
                        VALUES (?, ?, ?)
                    """, (user, user_type, user_password))

            except sqlite3.IntegrityError as e:
                print(f"Error inserting user {user}: {e}")
                continue

    # Remove users
    for user in removed_users:
        cursor.execute("DELETE FROM users WHERE name = ?;", (user,))
        cursor.execute("DELETE FROM passwords WHERE username = ?;", (user,))  # Remove password if user is removed

    # Modify users
    for user, changes in modified_users.items():
        cursor.execute("""
            UPDATE users SET 
                is_enabled = ?, access_level = ?, unit_group = ?, language = ?, remote_access = ?, 
                hide_inaccessible_resources = ?, can_change_own_password = ?, is_ldap_user = ?, 
                currently_in_ldap = ?
            WHERE name = ?;
        """, (*changes["new"], user))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sync.py <local_db> <remote_db>")
        sys.exit(1)

    local_db = sys.argv[1]  
    remote_db = sys.argv[2]  

    print(f"Comparing: Local DB = {local_db}, Remote DB = {remote_db}")

    local_users = get_users(local_db)
    remote_users = get_users(remote_db)
    local_passwords = get_passwords(local_db)  

    print(f"Local Users: {local_users}")
    print(f"Remote Users: {remote_users}")

    added, removed, modified = compare_users(local_users, remote_users)

    print("\n=== Added Users ===")
    for user, data in added.items():
        print(f"{user}: {data}")

    print("\n=== Removed Users ===")
    for user, data in removed.items():
        print(f"{user}: {data}")

    print("\n=== Modified Users ===")
    for user, changes in modified.items():
        print(f"{user}: OLD {changes['old']} -> NEW {changes['new']}")

    update_remote_db(local_db, added, removed, modified, local_passwords)  
    print("\nRemote database updated successfully!")
