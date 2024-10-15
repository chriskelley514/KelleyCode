import time

# Dictionary to store valid user credentials (username: password)
users = {"admin": "password123"}

# Track total failed attempts and lockout time
total_failed_attempts = 0
LOCKOUT_TIME = 30  # Lockout duration in seconds
MAX_ATTEMPTS = 3   # Maximum allowed login attempts (correct or incorrect)

# Variable to track lockout status
lockout_end_time = 0

# Function to handle login attempts
def login(username, password):
    global total_failed_attempts, lockout_end_time
    current_time = time.time()

    # Check if the lockout period hasn't expired
    if current_time < lockout_end_time:
        time_remaining = lockout_end_time - current_time
        print(f"Account is temporarily locked. Try again in {int(time_remaining)} seconds.")
        return False

    # Check if the username and password are correct
    if username in users and users[username] == password:
        print("Login successful!")
        total_failed_attempts = 0  # Reset attempts on successful login
        return True
    else:
        print("Incorrect username or password.")
        total_failed_attempts += 1
        print(f"Failed attempts: {total_failed_attempts}")

        # Lockout if total failed attempts exceed the max
        if total_failed_attempts >= MAX_ATTEMPTS:
            lockout_end_time = current_time + LOCKOUT_TIME
            print(f"Too many failed attempts. Account locked for {LOCKOUT_TIME} seconds.")
        return False

# Example loop to simulate login attempts
while True:
    # Prompt user for username and password input
    user = input("Username: ")
    pwd = input("Password: ")

    # Attempt login and break loop if successful
    if login(user, pwd):
        break
