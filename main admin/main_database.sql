-- Create the database
CREATE DATABASE smart_lock_system;
USE smart_lock_system;

-- Create the secure logging table
CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50),      -- e.g., 'SUCCESSFUL_LOGIN', 'FAILED_ATTEMPT'
    description TEXT,             -- e.g., 'User Admin entered correct PIN'
    prev_hash VARCHAR(64),        -- The SHA-256 hash of the row before this one
    current_hash VARCHAR(64)      -- The SHA-256 hash of (Data + prev_hash)
);

