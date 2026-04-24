# 🔐 Tamper-Evident Logging System

A cybersecurity-focused logging system designed to detect unauthorized modifications, deletions, or tampering in log data using cryptographic techniques.

---

## 🚀 Overview

Traditional logging systems store records as independent entries, making them vulnerable to **log tampering and deletion attacks**.

This project implements a **tamper-evident logging mechanism** where each log entry is cryptographically linked to the previous one using **SHA-256 hashing**, ensuring that any change in historical data is immediately detectable.

---

## 🎯 Key Features

* 🔗 **Hash Chaining (SHA-256)**
  Each log is linked to the previous log, forming a secure chain.

* 🔍 **Integrity Verification Engine**
  Detects:

  * Data modification
  * Log deletion
  * Sequence reordering

* 📊 **Forensic Excel Reports**

  * 🔴 Red → Data tampering
  * 🌸 Pink → Chain break

* 🔒 **Secure Log Archival (Fernet Encryption)**
  Logs are encrypted before deletion to preserve forensic evidence.

* 🛡️ **Role-Based Access Control (RBAC)**

  * `locker_admin` → INSERT, SELECT only
  * `main_admin` → Full access for audit & maintenance

---

## 🧠 Core Concept

Each log entry is generated as:

```text
Hash(current) = SHA256(timestamp + event_type + description + prev_hash)
```

This creates a **dependency chain**, where:

* Changing any log → breaks all subsequent hashes
* Deleting a log → breaks the chain

---

## 🏗️ System Architecture

```text
GUI (Tkinter)
      ↓
Logging Engine (Python + SHA-256)
      ↓
MySQL Database (RBAC)
      ↓
Verification Module
      ↓
Excel Forensic Report
```

---

## ⚙️ Tech Stack

* **Programming:** Python
* **Database:** MySQL
* **Cryptography:** SHA-256, Fernet (AES-based encryption)
* **Libraries:** Pandas, OpenPyXL, Cryptography
* **GUI:** Tkinter

---

## 📂 Project Structure

```text
├── main.py                # Logging engine (hash chaining)
├── gui_app.py             # User interface (PIN-based access)
├── verify_logs.py         # Integrity verification
├── export_excel.py        # Forensic report generation
├── admin_tools.py         # Secure archival & wipe
├── config.py              # Environment-based configuration
├── requirements.txt       # Dependencies
├── sample_outputs/        # Sample Excel reports
├── docs/                  # Project documentation
└── .env.example           # Environment variable template
```

---

## 🔧 Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/swee32/Tamper-Evident-Logging-System.git
cd Tamper-Evident-Logging-System
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_USER=locker_admin
DB_PASSWORD=your_password
DB_NAME=smart_lock_system

SECRET_PIN=1234
SECRET_KEY=your_generated_key
```

---

### 4️⃣ Run the application

```bash
python gui_app.py
```

---

## 🔍 Usage Workflow

1. Enter PIN via GUI → log generated
2. Logs stored with cryptographic chaining
3. Run verification:

```bash
python verify_logs.py
```

4. Generate forensic report:

```bash
python export_excel.py
```

5. Perform secure archival:

```bash
python admin_tools.py
```

---

## 📊 Detection Capabilities

| Attack Type    | Detection Method   | Result      |
| -------------- | ------------------ | ----------- |
| Data Tampering | Hash mismatch      | 🔴 Detected |
| Log Deletion   | Chain break        | 🌸 Detected |
| Reordering     | Hash inconsistency | 🌸 Detected |

---

## 🔐 Security Considerations

* No sensitive credentials are stored in the repository
* Uses environment variables (`.env`) for configuration
* Encryption keys are not exposed
* Key fingerprinting is used for safe verification

---

## 📸 Sample Output

Check `sample_outputs/` for:

* Secure log reports
* Tampered vs clean log comparison

---

## 🎓 Project Context

Final Year Engineering Project
Domain: **Cybersecurity & Digital Forensics**

---

## 🚀 Future Improvements

* Cloud deployment (AWS EC2 / S3 integration)
* Real-time alert system (Email / Telegram)
* Web-based dashboard
* SIEM integration

---

## 👩‍💻 Author

**Sweety Kamble**
Final Year Engineering Student (EnTC)
Aspiring Cloud Engineer

---

## ⭐ If you found this project useful, consider giving it a star!
