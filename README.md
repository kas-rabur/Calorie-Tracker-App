# Secure Calorie Tracker (Client-Server Application)

This project is a secure, networked calorie tracking system built with Python. It allows users to register, log in, track food intake, and manage user data through a graphical interface. Admin users can monitor client activity and logs.

## Features

### ✅ Functional Requirements
- Login and registration system with hashed passwords and salt using **scrypt**.
- GUI-based client built with **CustomTkinter**.
- Secure SSL/TLS encrypted communication using custom certificates.
- Diffie-Hellman key exchange for secure shared key generation.
- Persistent storage with **SQLite** for user credentials and food data.
- Calorie tracker showing current day consumption and remaining allowance.
- Admin panel with log viewing and user list access.
- Handles disconnections, multiple clients, and various input errors.
- Logging of all major server events to `server.log`.

### 🔐 Security Highlights
- SSL certificates used (`server.crt`, `server.key`) to encrypt network communication.
- Parameterized SQL queries to prevent injection attacks.
- Account lockout after 4 failed login attempts.
- Logging of login attempts and data access for audit purposes.

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install pycryptodome
pip install customtkinter
pip install asyncio
```
### 2. Run application

```bash
python server.py
python client.py
```
### 3. Admin Login (Purely for Testing)
```bash
username: admin
password: adminpass
```
## Files Overview

| File             | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `server.py`      | Handles all backend logic including SSL, client management, and database ops |
| `client.py`      | Frontend GUI client using CustomTkinter with login, register, and tracker UI |
| `userdata.db`    | SQLite database storing users, salts, and food intake logs                   |
| `server.crt`     | SSL certificate for secure server-client communication                       |
| `server.key`     | SSL private key for server encryption                                        |
| `openssl.cnf`    | Configuration file used when generating SSL certificates                     |
| `server.log`     | Log file that records events like logins, data fetches, and errors           |
| `checklist.txt`  | Marked project requirements showing implemented networking and security tasks |
| `README.md`      | Documentation and setup instructions for running and testing the application |
