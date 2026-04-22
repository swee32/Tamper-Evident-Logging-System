import mysql.connector
import hashlib
import config

def verify_integrity_check():
    """
    Returns True if the database is secure, False if tampered.
    This function is used by admin_tools.py before performing backups.
    """
    try:
        db = mysql.connector.connect(**config.DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM access_logs ORDER BY id ASC")
        logs = cursor.fetchall()

        if not logs:
            return True # Empty database is technically 'secure'

        last_stored_hash = "0" * 64 
        
        for row in logs:
            # 1. Chain Link Check
            if row['prev_hash'] != last_stored_hash:
                print(f"❌ CHAIN BROKEN: Missing or reordered data at ID {row['id']}")
                return False
            
            # 2. Content Integrity Check
            data_to_verify = f"{row['timestamp']}{row['event_type']}{row['description']}{row['prev_hash']}"
            recalculated_hash = hashlib.sha256(data_to_verify.encode()).hexdigest()
            
            if row['current_hash'] != recalculated_hash:
                print(f"❌ DATA TAMPERED: Modification detected at ID {row['id']}")
                return False
                
            last_stored_hash = row['current_hash']

        db.close()
        return True
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

if __name__ == "__main__":
    # If run directly, just print the result
    if verify_integrity_check():
        print("✅ DATABASE INTEGRITY VERIFIED: All logs are secure.")
    else:
        print("🛑 SYSTEM ALERT: Integrity compromised!")