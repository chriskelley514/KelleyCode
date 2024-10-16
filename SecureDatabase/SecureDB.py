import sqlite3
from cryptography.fernet import Fernet

# Generate a key for encryption/decryption
# Save this key securely in production
key = Fernet.generate_key()
cipher = Fernet(key)

# Hardcoded master login credentials (for demonstration)
MASTER_USERNAME = "admin"
MASTER_PASSWORD = "masterpass"

# Create the encrypted database and the users table
def create_database():
    conn = sqlite3.connect('encrypted_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert encrypted data into the database
def insert_user(name: str, age: str, username: str, password: str):
    encrypted_name = cipher.encrypt(name.encode())
    encrypted_age = cipher.encrypt(age.encode())
    encrypted_username = cipher.encrypt(username.encode())
    encrypted_password = cipher.encrypt(password.encode())
    
    conn = sqlite3.connect('encrypted_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, age, username, password)
        VALUES (?, ?, ?, ?)
    ''', (encrypted_name, encrypted_age, encrypted_username, encrypted_password))
    conn.commit()
    conn.close()
    print("User data has been encrypted and stored in the database.\n")

# Retrieve and decrypt a user entry by username
def retrieve_user_by_username(search_username: str):
    conn = sqlite3.connect('encrypted_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, age, username, password FROM users')
    rows = cursor.fetchall()
    
    for row in rows:
        decrypted_username = cipher.decrypt(row[2]).decode()
        
        if decrypted_username == search_username:
            decrypted_name = cipher.decrypt(row[0]).decode()
            decrypted_age = cipher.decrypt(row[1]).decode()
            decrypted_password = cipher.decrypt(row[3]).decode()
            
            print(f"\n--- User Found ---")
            print(f"Name: {decrypted_name}")
            print(f"Age: {decrypted_age}")
            print(f"Username: {decrypted_username}")
            print(f"Password: {decrypted_password}\n")
            conn.close()
            return
    print("No user found with that username.\n")
    conn.close()

# Master login to access user data
def master_login():
    print("\n--- Master Login ---")
    username = input("Enter master username: ")
    password = input("Enter master password: ")
    
    if username == MASTER_USERNAME and password == MASTER_PASSWORD:
        print("Master login successful.\n")
        return True
    else:
        print("Master login failed.\n")
        return False

# Main menu
def menu():
    while True:
        print("1. Add new user")
        print("2. Search for user by username (requires master login)")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == "1":
            # Add a new user
            name = input("Enter name: ")
            age = input("Enter age: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            insert_user(name, age, username, password)
        
        elif choice == "2":
            # Master login to search for a user
            if master_login():
                search_username = input("Enter the username to search for: ")
                retrieve_user_by_username(search_username)
        
        elif choice == "3":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    # Create the database and the table if they don't exist
    create_database()
    
    # Run the menu system
    menu()
