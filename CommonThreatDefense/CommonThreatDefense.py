import re
import hashlib
import os
import hmac
from html import escape
import sqlite3

# Secure hash with salt for password storage
def hash_password(password: str) -> str:
    salt = os.urandom(16)  # Generate a random salt
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + hash_obj.hex()

# Verifying password against stored hash
def verify_password(stored_password: str, provided_password: str) -> bool:
    salt = bytes.fromhex(stored_password[:32])
    stored_hash = stored_password[32:]
    hash_obj = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return hmac.compare_digest(stored_hash, hash_obj.hex())

# Input validation for usernames (to prevent SQL injection)
def validate_username(username: str) -> bool:
    return bool(re.match("^[a-zA-Z0-9_]{3,30}$", username))  # Alphanumeric and underscore only

# Input sanitization for web forms (escaping special HTML characters)
def sanitize_input(user_input: str) -> str:
    return escape(user_input)

# Function to create the 'users' table if it doesn't exist
def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()

# SQL injection prevention using parameterized queries
def add_user_to_db(username: str, password: str):
    if not validate_username(username):
        raise ValueError("Invalid username format.")
    
    hashed_password = hash_password(password)
    conn = sqlite3.connect('secure_app.db')
    
    # Ensure the 'users' table exists
    create_users_table(conn)

    cursor = conn.cursor()
    
    # Using parameterized queries to prevent SQL injection
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    print("User added successfully.")

# Function to prevent cross-site scripting (XSS)
def display_comment(comment: str) -> str:
    return sanitize_input(comment)  # Escapes HTML tags to prevent XSS

# Error handling to avoid leaking sensitive information (example: division by zero)
def safe_divide(a: int, b: int) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        return None

# Main program to demonstrate the security features
if __name__ == "__main__":
    # Example of secure password storage and user management
    username = "secure_user"
    password = "StrongP@ssw0rd!"
    
    try:
        add_user_to_db(username, password)
    except ValueError as ve:
        print(f"Error: {ve}")

    # Demonstrating protection against XSS
    comment = "<script>alert('XSS Attack!');</script>"
    print("Sanitized Comment: ", display_comment(comment))

    # Demonstrating error handling
    result = safe_divide(10, 0)
    if result is not None:
        print(f"Result: {result}")
