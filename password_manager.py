import mysql.connector as sqltor
import maskpass
from cryptography.fernet import Fernet
import os

# =========================
# KEY SETUP
# =========================

KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
fernet = Fernet(key)

# =========================
# DB PASSWORD
# =========================

DB_PASSWORD = maskpass.askpass("Enter MySQL password: ")

# =========================
# DATABASE INIT
# =========================

def init_db():
    temp_con = sqltor.connect(
        host='localhost',
        user='root',
        passwd=DB_PASSWORD
    )
    temp_cursor = temp_con.cursor()

    temp_cursor.execute("CREATE DATABASE IF NOT EXISTS passwd")
    temp_cursor.execute("USE passwd")

    temp_cursor.execute("""
    CREATE TABLE IF NOT EXISTS userpas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username BLOB,
        passwd BLOB
    )
    """)

    temp_cursor.execute("""
    CREATE TABLE IF NOT EXISTS store (
        id INT,
        website BLOB,
        username BLOB,
        passwd BLOB
    )
    """)

    temp_con.commit()
    temp_cursor.close()
    temp_con.close()

init_db()

# =========================
# MAIN DB CONNECTION
# =========================

con = sqltor.connect(
    host='localhost',
    user='root',
    passwd=DB_PASSWORD,
    database='passwd'
)
cursor = con.cursor()

# =========================
# FUNCTIONS
# =========================

def add_password(user_id):
    website = input("Enter website name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    enc_website = fernet.encrypt(website.encode())
    enc_username = fernet.encrypt(username.encode())
    enc_password = fernet.encrypt(password.encode())

    query = "INSERT INTO store (id, website, username, passwd) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, enc_website, enc_username, enc_password))
    con.commit()

    print("Password added successfully!")

# -------------------------

def display_passwords(user_id):
    query = "SELECT website, username, passwd FROM store WHERE id = %s"
    cursor.execute(query, (user_id,))
    records = cursor.fetchall()

    if records:
        print("\nStored passwords:")
        for record in records:
            dec_website = fernet.decrypt(record[0]).decode()
            dec_username = fernet.decrypt(record[1]).decode()
            dec_password = fernet.decrypt(record[2]).decode()
            print(f"Website: {dec_website}, Username: {dec_username}, Password: {dec_password}")
    else:
        print("No records found.")

# -------------------------

def update_password(user_id):
    display_passwords(user_id)
    website = input("Enter website name to update: ")

    query = "SELECT website, username, passwd FROM store WHERE id = %s"
    cursor.execute(query, (user_id,))
    records = cursor.fetchall()

    for record in records:
        if fernet.decrypt(record[0]).decode() == website:
            print("1. Update Username")
            print("2. Update Password")
            choice = input("Enter choice: ")

            if choice == "1":
                new_username = input("Enter new username: ")
                enc = fernet.encrypt(new_username.encode())
                cursor.execute(
                    "UPDATE store SET username=%s WHERE id=%s AND website=%s",
                    (enc, user_id, record[0])
                )

            elif choice == "2":
                new_password = input("Enter new password: ")
                enc = fernet.encrypt(new_password.encode())
                cursor.execute(
                    "UPDATE store SET passwd=%s WHERE id=%s AND website=%s",
                    (enc, user_id, record[0])
                )

            con.commit()
            print("Updated successfully!")
            return

    print("No matching record found.")

# -------------------------

def find_password(user_id):
    website = input("Enter website name to search: ")

    query = "SELECT website, username, passwd FROM store WHERE id = %s"
    cursor.execute(query, (user_id,))
    records = cursor.fetchall()

    found = False

    for record in records:
        dec_website = fernet.decrypt(record[0]).decode()
        if website.lower() in dec_website.lower():
            dec_username = fernet.decrypt(record[1]).decode()
            dec_password = fernet.decrypt(record[2]).decode()

            print(f"Website: {dec_website}, Username: {dec_username}, Password: {dec_password}")
            found = True

    if not found:
        print("No matching records found.")

# =========================
# MENU
# =========================

def main_menu(user_id):
    while True:
        print("""
1. Add new password
2. See stored passwords
3. Update existing password
4. Find record
5. Exit
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            add_password(user_id)
        elif choice == "2":
            display_passwords(user_id)
        elif choice == "3":
            update_password(user_id)
        elif choice == "4":
            find_password(user_id)
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid input.")

# =========================
# AUTH SYSTEM (FIXED LOGIN ONLY)
# =========================

def authenticate():
    print("\nPASSWORD MANAGEMENT SYSTEM\n")

    print("1. Login")
    print("2. Signup")
    choice = input("Enter choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = maskpass.askpass("Enter password: ", mask="*")

        cursor.execute("SELECT id, username, passwd FROM userpas")
        records = cursor.fetchall()

        for record in records:
            dec_username = fernet.decrypt(record[1]).decode()
            dec_password = fernet.decrypt(record[2]).decode()

            if dec_username == username and dec_password == password:
                print("Login successful!")
                main_menu(record[0])
                return

        print("Invalid username or password.")

    elif choice == "2":
        username = input("Enter username: ")
        password = maskpass.askpass("Enter password: ", mask="*")
        password_ver = maskpass.askpass("Re-enter password: ", mask="*")

        if password == password_ver:
            enc_username = fernet.encrypt(username.encode())
            enc_password = fernet.encrypt(password.encode())

            cursor.execute(
                "INSERT INTO userpas (username, passwd) VALUES (%s, %s)",
                (enc_username, enc_password)
            )
            con.commit()

            print("Signup successful! Please login.")
            authenticate()
        else:
            print("Passwords do not match.")

    else:
        print("Invalid choice.")

# =========================
# RUN PROGRAM
# =========================

if __name__ == "__main__":
    authenticate()
