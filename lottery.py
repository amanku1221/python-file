import time
import random
import threading
import signal
import string
import os
from datetime import datetime, timedelta

# Globals
users = set()
lock = threading.Lock()
log_file = 'lottery_log.txt'
backup_file = 'backup_users.txt'
start_time = datetime.now()
registration_period = timedelta(minutes=1)  # change to 60 for 1 hour in real run
extended_period = timedelta(minutes=30)
next_backup_time = time.time() + 300  # every 5 minutes
registration_end_time = start_time + registration_period
extended = False
running = True

# Create log file
def log(msg):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

# Save backup of users
def save_backup():
    with open(backup_file, 'w') as f:
        for user in users:
            f.write(f"{user}\n")

# Load backup users if file exists
def load_backup():
    if os.path.exists(backup_file):
        with open(backup_file, 'r') as f:
            for line in f:
                users.add(line.strip())

# Display remaining time every 10 minutes
def time_announcer():
    while running:
        time.sleep(600)  # every 10 minutes
        with lock:
            if running:
                time_left = max((registration_end_time - datetime.now()).total_seconds(), 0)
                mins = int(time_left // 60)
                print(f"\n[INFO] Time remaining for registration: {mins} minute(s)")
                print(f"[INFO] Registered users: {len(users)}\n")

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print("\n[INFO] Program interrupted. Saving progress...")
    with lock:
        save_backup()
        log("Program interrupted. Backup saved.")
        print("[INFO] Backup saved. Exiting.")
    exit(0)

# Validate username
def is_valid_username(username):
    if not username:
        return False
    allowed = string.ascii_letters + string.digits + "_"
    return all(char in allowed for char in username)

# Registration logic
def register_users():
    global registration_end_time, extended, running, next_backup_time
    while datetime.now() < registration_end_time:
        username = input("Enter a unique username to register (or type 'exit' to quit): ").strip()

        if username.lower() == 'exit':
            print("[INFO] Exiting registration early...")
            running = False
            save_backup()
            return

        if not is_valid_username(username):
            print("[ERROR] Invalid username. Use letters, digits, and underscores only.")
            continue

        with lock:
            if username in users:
                print("[ERROR] Username already registered.")
                continue

            users.add(username)
            log(f"User registered: {username}")
            print(f"[INFO] {username} registered successfully. Total users: {len(users)}")

        # Save backup every 5 minutes
        if time.time() > next_backup_time:
            with lock:
                save_backup()
            next_backup_time = time.time() + 300

    # Extension check
    if len(users) < 5 and not extended:
        print("\n[INFO] Less than 5 users registered. Extending registration by 30 minutes...")
        registration_end_time = datetime.now() + extended_period
        extended = True
        register_users()  # Call again for extension
    elif len(users) == 0:
        print("[INFO] No users registered. Exiting.")
        log("No users registered. Lottery ended with no participants.")
        running = False
        return

# Pick and announce winner
def pick_winner():
    print("\n[INFO] Registration period ended.")
    if len(users) == 0:
        print("[INFO] No participants. Exiting.")
        return

    winner = random.choice(list(users))
    print("\n🎉🎉🎉 Lottery Winner 🎉🎉🎉")
    print(f"Winner: {winner}")
    print(f"Total Participants: {len(users)}")
    print("Thank you for participating!")

    log(f"Winner declared: {winner}")
    log(f"Total Participants: {len(users)}")

    # Clean up backup file
    if os.path.exists(backup_file):
        os.remove(backup_file)

# Main function
def main():
    print("=== Welcome to the Terminal Lottery System ===")
    print("Registration is open for 1 hour (currently set to 2 minutes for testing).")
    print("Enter a valid and unique username to join.")
    print("You can type 'exit' at any time to stop.")

    signal.signal(signal.SIGINT, signal_handler)
    load_backup()

    # Start time announcer thread
    announcer = threading.Thread(target=time_announcer, daemon=True)
    announcer.start()

    # Begin registration
    register_users()

    # Draw winner
    if running:
        pick_winner()

if __name__ == "__main__":
    main()
