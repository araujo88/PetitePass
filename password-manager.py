import os
import bcrypt
from utils import *
from playhouse.sqlcipher_ext import *
from database import *

if __name__ == "__main__":

    is_auth = False

    if not os.path.isfile('./password'):
        while True:
            password_input = getpass.getpass("Please create a password: ")

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

        # Create a password database for the first time
        db = SqlCipherDatabase('passwords.db', passphrase=password_input)
        Password.create_table()
        # Encode password
        password = str.encode(password_input)
        # Hash a password for the first time, with a randomly-generated salt
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        f = open("password", "w")
        # digest = hashlib.sha256(hashed).hexdigest()
        f.write(hashed.decode())
        f.close()
        is_auth = True
    else:
        password_input = getpass.getpass("Please input your password: ")
        password = str.encode(password_input)
        f = open("password")
        hashed = str.encode(f.readline())
        # Check that an unhashed password matches one that has previously been hashed
        if bcrypt.checkpw(password, hashed):
            print("The password entered is correct.")
            is_auth = True
        else:
            print("The password is incorrect.")
            is_auth = False

    if is_auth:
        print("You are now authenticated. Welcome to password manager!")
        while(True):
            print("\n--------------------------------")
            print("Please input the desired option:\n")
            print("(6) - List registered passwords")
            print("(5) - Register a new password record")
            print("(4) - Update a password record")
            print("(3) - Delete a password record")
            print("(2) - Check password security")
            print("(1) - Generate secure password")
            print("(0) - Exit")
            print("--------------------------------\n")
            user_input = input()

            if user_input == '1':
                cls()
                generate_password()

            elif user_input == '2':
                cls()
                verify_password()

            elif user_input == '3':
                cls()
                delete_password()

            elif user_input == '4':
                cls()
                update_password()

            elif user_input == '5':
                cls()
                create_password()

            elif user_input == '6':
                cls()
                print_passwords()

            elif user_input == '0':
                cls()
                print("Exiting program ...")
                break

            else:
                cls()
                print("Invalid option.")
