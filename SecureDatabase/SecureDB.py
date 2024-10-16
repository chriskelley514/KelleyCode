import sqlite3
import time
from cryptography.fernet import Fernet
import os

# Path to the key file
KEY_FILE = "secret.key"

# Function to load or generate a key
def load_or_generate_key():
    # Check if the key already exists in the file
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    else:
        # Generate a new key and save it to a file
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    return key

# Load the encryption key from the file
key = load_or_generate_key()
cipher = Fernet(key)

# Create the encrypted database and the users table
def create_database():
    conn = sqlite3.connect('encrypted_database.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
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

# Check if the username already exists in the database
def username_exists(username: str):
    conn = sqlite3.connect('encrypted_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users')
    rows = cursor.fetchall()
    
    for row in rows:
        decrypted_username = cipher.decrypt(row[0]).decode()
        if decrypted_username == username:
            return True
    return False

# Insert encrypted data into the database
def insert_user(name: str, age: str, username: str, password: str):
    # Check if the username already exists
    if username_exists(username):
        print("Error: Username already exists. Please choose a different username.\n")
        return

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
        try:
            decrypted_username = cipher.decrypt(row[2]).decode()
            if decrypted_username == search_username:
                decrypted_name = cipher.decrypt(row[0]).decode()
                decrypted_age = cipher.decrypt(row[1]).decode()
                decrypted_password = cipher.decrypt(row[3]).decode()
                
                return {
                    "name": decrypted_name,
                    "age": decrypted_age,
                    "username": decrypted_username,
                    "password": decrypted_password
                }
        except cryptography.fernet.InvalidToken:
            print("Decryption failed. Invalid data or key mismatch.")
            return None

    return None

# Validate username and password for login
def validate_login(username: str, password: str):
    user_data = retrieve_user_by_username(username)
    if user_data is None:
        return False

    if user_data['password'] == password:
        print("\nLogin successful!")
        print(f"Name: {user_data['name']}")
        print(f"Age: {user_data['age']}")
        print(f"Username: {user_data['username']}")
        print(f"Password: {user_data['password']}\n")
        return True
    else:
        return False

# Function to handle login with brute-force protection and "back" option
def user_login():
    MAX_ATTEMPTS = 3
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        print("Type 'back' to return to the main menu.")
        username = input("Enter your username: ")
        if username.lower() == "back":
            return False  # Return to the main menu

        password = input("Enter your password: ")
        if password.lower() == "back":
            return False  # Return to the main menu

        if validate_login(username, password):
            return True
        else:
            attempts += 1
            print(f"Incorrect username or password. {MAX_ATTEMPTS - attempts} attempts left.\n")
            
            if attempts >= MAX_ATTEMPTS:
                print("Too many failed attempts. You are locked out for 30 seconds.\n")
                time.sleep(30)  # Lock out for 30 seconds
                return False

# Main menu
def menu():
    while True:
        print("1. Add new user")
        print("2. User login")
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
            # Login the user
            if user_login():
                print("Welcome to your account.\n")
            else:
                print("Returning to main menu.\n")
        
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
