import mysql.connector
import hashlib
from datetime import datetime

import config

# 1. Database Connection
def get_db_connection():
    return mysql.connector.connect(**config.DB_CONFIG) # Uses the locker_admin credentials


# 2. Hashing Logic (The "Security Linkage")
def calculate_hash(data_string):
    return hashlib.sha256(data_string.encode()).hexdigest()

# 3. Function to Add a Log (Tamper-Evident Style)
def add_access_log(event_type, description):
    db = get_db_connection()
    cursor = db.cursor()

    # Get the hash of the VERY LAST entry to link them
    cursor.execute("SELECT current_hash FROM access_logs ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    
    # If it's the first log ever, use a 'Genesis' hash of zeros
    prev_hash = result[0] if result else "0" * 64

    # Combine data to create the new hash
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_to_hash = f"{timestamp}{event_type}{description}{prev_hash}"
    current_hash = calculate_hash(data_to_hash)

    # Insert into MySQL
    query = "INSERT INTO access_logs (event_type, description, prev_hash, current_hash) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (event_type, description, prev_hash, current_hash))
    
    db.commit()
    print(f"✅ Log Added: {event_type} | Hash: {current_hash[:10]}...")
    db.close()

# --- SIMULATION ---
if __name__ == "__main__":
    # Simulate a few events
    add_access_log("SUCCESSFUL_LOGIN", "User: Admin entered correct PIN")
    add_access_log("FAILED_ATTEMPT", "User: Unknown tried PIN 1234")