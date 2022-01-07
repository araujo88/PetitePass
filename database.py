import datetime
import getpass
import os
from utils import *
import bcrypt

from playhouse.sqlcipher_ext import *


class Password(Model):
    name = TextField()
    password = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(null=True)

    class Meta:
        if not os.path.isfile('./passwords.db'):
            while True:
                while True:
                    password_input0 = getpass.getpass(
                        "Please create a password: ")
                    password_input = getpass.getpass(
                        "Please confirm your password: ")
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
                    print(
                        "Error: your password must contain at least one special character.")
                elif any(i in ONLY_LOWERCASE for i in password_input) == False:
                    print(
                        "Error: your password must contain at least one lower-case character.")
                elif any(i in ONLY_UPPERCASE for i in password_input) == False:
                    print(
                        "Error: your password must contain at least one upper-case character.")
                elif entropy_ratio < 90:
                    print("Error: your password is too simple.")
                else:
                    break

            # Encode password
            password = str.encode(password_input)
            # Hash a password for the first time, with a randomly-generated salt
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            f = open("password", "w")
            # digest = hashlib.sha256(hashed).hexdigest()
            f.write(hashed.decode())
            f.close()
            is_auth = True
            db = SqlCipherDatabase('passwords.db', passphrase=password_input)
            database = db
        else:
            password_input = getpass.getpass('Enter the database password: ')
            password = str.encode(password_input)
            f = open("password")
            hashed = str.encode(f.readline())
            # Check that an unhashed password matches one that has previously been hashed
            if bcrypt.checkpw(password, hashed):
                print("The password entered is correct.")
                db = SqlCipherDatabase(
                    'passwords.db', passphrase=password_input)
                database = db
                is_auth = True
            else:
                print("The password is incorrect.")
                is_auth = False


def create_password():
    try:
        print("Input the password identification name:")
        input_name = input()
        print("Input the matching password:")
        input_password = input()
        Password.create(name=input_name, password=input_password)
    except:
        print("An error occurred.")
    else:
        print("Password record created successfully!")


def print_passwords():
    try:
        print("Registered passwords:\n")
        for password in Password.select():
            print(
                f"Name: {password.name} | Password: {password.password} | Created: {password.timestamp} | Updated: {password.updated}")
    except:
        print("An error occurred.")


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
    except:
        print("An error occurred.")
    else:
        print("Password updated successfully!")


def delete_password():
    try:
        print("Input the password identification name to be deleted:")
        input_name = input()
        password = Password.get(Password.name == input_name)
        password.delete_instance()
    except:
        print("An error occurred.")
    else:
        print("Record deleted successfully!")
