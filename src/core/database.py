import datetime
import getpass
import os
from core.utils import *
import bcrypt
from tabulate import tabulate
import numpy as np
from playhouse.sqlcipher_ext import *


class Password(Model):
    name = TextField()
    username = TextField(null=True)
    password = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(null=True)

    class Meta:
        pass

def create_password(input_name, input_username, input_passowrd):
    try:
        if Password.get(Password.name == input_name) is not None:
            print(
                "The name already exists! Please type another name for the password.")
        else:
            Password.create(
                name=input_name, username=input_username, password=input_passowrd)
    except Exception as e:
        Password.create(
            name=input_name, username=input_username, password=input_passowrd)
    else:
        print("Password record created successfully!")


def print_passwords():
    print("Registered passwords:\n")
    d = np.zeros((Password.select().count(), 5), dtype=object)
    i = 0
    for password in Password.select():
        d[i, :] = [password.name, password.username, password.password,
                   password.timestamp, password.updated]
        i += 1
    print(tabulate(d, headers=["Id", "Username",
          "Password", "Created", "Updated"]))


def update_password():
    try:
        print("Input the password identification name to be updated:")
        input_name = input()
        password = Password.get(Password.name == input_name)
        print("Input the new password:")
        new_password = input()
        password.password = new_password
        password.updated = datetime.datetime.now()
        password.save()
    except Exception as e:
        print("An error occurred:")
        print(e)
    else:
        print("Password updated successfully!")


def delete_password():
    try:
        print("Input the password identification name to be deleted:")
        input_name = input()
        password = Password.get(Password.name == input_name)
        password.delete_instance()
    except Exception as e:
        print(e)
    else:
        print("Record deleted successfully!")


def change_db_password():
    path = f"/home/{getpass.getuser()}/PetitePass"
    if not os.path.exists(path):
        os.makedirs(path)

    while True:
        current_password = getpass.getpass(
            'Please enter the current password: ')
        password = str.encode(current_password)
        passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"
        f = open(passwd_path)
        hashed = str.encode(f.readline())
        if bcrypt.checkpw(password, hashed):
            print("The password entered is correct.")
            break
        else:
            print("The password is incorrect.")

    while True:
        password_input0 = getpass.getpass("Please type the new password: ")
        password_input = getpass.getpass("Please confirm your password: ")
        if password_input0 == password_input:
            break
        else:
            print("The passwords don't match.")

        input_entropy = entropy(list(password_input), 10)
        input_ideal_entropy = entropy_ideal(len(password_input), 10)
        entropy_ratio = 100*input_entropy/input_ideal_entropy

        if len(password_input) < 8:
            print("Error: your password must be at least 8 characters long.")
        elif any(i in SPECIAL_CHARS for i in password_input) == False:
            print("Error: your password must contain at least one special character.")
        elif any(i in ONLY_LOWERCASE for i in password_input) == False:
            print("Error: your password must contain at least one lower-case character.")
        elif any(i in ONLY_UPPERCASE for i in password_input) == False:
            print("Error: your password must contain at least one upper-case character.")
        elif entropy_ratio < 85:
            print("Error: your password is too simple.")
        else:
            break

    password = str.encode(password_input)
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"
    f = open(passwd_path, "w")
    f.write(hashed.decode())
    f.close()
    database_path = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
    db = SqlCipherDatabase(database_path, passphrase=current_password)
    db.execute_sql(f"PRAGMA key = '{current_password}';")
    db.execute_sql(f"PRAGMA rekey = '{password_input}';")
    print("Password modified! Please restart the password manager.")
    exit()
