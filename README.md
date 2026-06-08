# 🔐 Password Manager (Python + MySQL)

A secure, CLI-based password manager built using Python and MySQL that allows users to store, retrieve, and manage credentials safely using **Fernet encryption**.

This project demonstrates concepts of:
- Authentication systems
- Encryption & basic cybersecurity
- Database management with MySQL
- CRUD operations in Python

---

## 📌 Features

- 👤 User Signup & Login system
- 🔐 Secure password storage using Fernet encryption
- 📂 Store website credentials (username + password)
- 🔎 Search saved credentials by website name
- ✏️ Update stored passwords or usernames
- 🗄️ MySQL database integration
- 🧾 Automatic database and table creation

---

## ⚙️ How It Works

- Users create an account and log in
- Login credentials are stored in the database (encrypted using Fernet)
- Each user has a unique ID to manage their stored passwords
- Website credentials are encrypted before storage
- Data is decrypted only when the authenticated user requests it
- A locally stored encryption key (`secret.key`) is used for encryption/decryption

---

## 🛠️ Tech Stack

- Python 🐍
- MySQL 🗄️
- Cryptography (Fernet) 🔐
- Maskpass (secure input handling) 🔑

---

## 📁 Project Structure

password-manager/
│
├── main.py              # Main application file
├── secret.key           # Auto-generated encryption key (DO NOT SHARE)
├── requirements.txt     # Dependencies
└── README.md            # Project documentation

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/password-manager.git
cd password-manager
```

### 2. Install dependencies
```bash
pip install mysql-connector-python cryptography maskpass
```

### 3. Setup MySQL
- Install MySQL server
- Start MySQL service locally
- Ensure you have a root user password
- The program will:
  - Create database automatically (`passwd`)
  - Create required tables (`userpas`, `store`)

### 4. Run the project
```bash
python main.py
```

---

## 🔐 Security Design

This project uses **symmetric encryption (Fernet)** to protect stored credentials.

### Key points:
- Encryption key is stored locally in `secret.key`
- Data is encrypted before storing in MySQL
- Data is decrypted only after user authentication

### ⚠️ Limitations:
- If both `database` and `secret.key` are compromised, data can be decrypted
- This is a **learning-level implementation**, not production-grade security

---

## 🧠 Concepts Learned

- Symmetric encryption (Fernet)
- Authentication flow design
- Database CRUD operations
- Secure user input handling
- Real-world system architecture basics

---

## 🚀 Future Improvements

- Replace login system with bcrypt hashing
- Implement PBKDF2/Argon2 key derivation
- Convert CLI app into web application
- Add password strength checker
- Use environment variables for configuration
- Add GUI interface (Tkinter / Flask)

---

## 👨‍💻 Author

Built by Ayush Kumar  
A learning project focused on understanding encryption, authentication, and database systems.

---

## 📌 Note

This project is intended for educational purposes only.
