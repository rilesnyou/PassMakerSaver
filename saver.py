import sqlite3
from hashlib import sha256

MAIN_PASS = "password"

connect = input("What is your password?\n")

while connect != MAIN_PASS:
    connect = input("What is your password?\n")
    if connect == "q":
        break

conn = sqlite3.connect('pass_manage.db')

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')
    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key + '"')
    conn.execute(command)
    conn.commit()
    return create_password(secret_key, service, admin_pass)

if connect == MAIN_PASS:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your password saver has been created.\n What would you like to add?")
    except:
        print("You have a saver already, what would you like to add?")

    while True:
        print("\n" + "*"*15)
        print("Commands:")
        print("q = quit")
        print("p = get password")
        print("sp = save password")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "sp":
            service = input("What is the password for?\n")
            print("\n" + service.capitalize() + " password created:\n" + add_password(service, MAIN_PASS))
        if input_ == "p":
            service = input("What is the password for?\n")
            print("\n" + service.capitalize() + " password:\n"+get_password(MAIN_PASS,service))