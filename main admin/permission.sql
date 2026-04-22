-- 1. Drop the user if they are stuck in a weird state
DROP USER IF EXISTS 'locker_admin'@'localhost';

-- 2. Re-create the user fresh
CREATE USER 'locker_admin'@'localhost' IDENTIFIED BY 'SecurePass123!';

-- 3. Grant ONLY standard usage (No DELETE, No TRUNCATE)
GRANT SELECT, INSERT ON smart_lock_system.access_logs TO 'locker_admin'@'localhost';

-- 4. Finalize
FLUSH PRIVILEGES;