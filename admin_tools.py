import mysql.connector
import os
import verify_logs 
from cryptography.fernet import Fernet
from datetime import datetime

# --- KEY MANAGEMENT ---
KEY_FILE = "secret.key"

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        new_key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(new_key)
        return new_key

# Initialize the cipher with a valid 32-byte key
KEY = load_or_generate_key()
cipher_suite = Fernet(KEY)
# ----------------------

def secure_admin_wipe():
    # --- STEP A: VERIFY ---
    print("🔍 [PHASE 1] Running integrity check...")
    if not verify_logs.verify_integrity_check():
        print("🛑 WIPE ABORTED: The current logs are tampered!")
        print("You cannot backup or delete data while the chain is broken.")
        return

    # --- STEP B: BACKUP & ENCRYPT ---
    print("🔒 [PHASE 2] Integrity verified. Creating encrypted backup...")
    try:
        # Use root or main admin for this high-level task
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="S322003y#", # Main Admin Credentials
            database="smart_lock_system"
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM access_logs")
        logs = cursor.fetchall()

        if not logs:
            print("ℹ️ No logs to backup.")
            return

        # Prepare data for encryption
        log_data_string = str(logs).encode()
        encrypted_data = cipher_suite.encrypt(log_data_string)

        # Ensure backup folder exists
        if not os.path.exists("backups"):
            os.makedirs("backups")

        # Save the encrypted file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backups/secure_archive_{timestamp}.enc"
        with open(filename, "wb") as f:
            f.write(encrypted_data)

        # --- STEP C: CLEAR ---
        print(f"🧹 [PHASE 3] Backup saved to {filename}. Clearing active table...")
        cursor.execute("TRUNCATE TABLE access_logs")
        db.commit()
        
        print("\n✅ SYSTEM RESET COMPLETE.")
        print(f"🔑 MAIN ADMIN KEY TO DECRYPT THIS BACKUP: {KEY.decode()}")
        db.close()

    except Exception as e:
        print(f"❌ Error during admin wipe: {e}")

if __name__ == "__main__":
    print("\n--- 🛡️ MAIN ADMIN SECURITY PORTAL ---")
    confirm = input("Are you sure you want to Wipe and Archive all logs? (y/n): ")
    if confirm.lower() == 'y':
        secure_admin_wipe()