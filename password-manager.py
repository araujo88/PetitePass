# Todo 1: generate passwords with restricted characters
# Todo 2: check for english words
# Todo 3: check for common passwords

import os
from utils import *
from playhouse.sqlcipher_ext import *
from database import *


if __name__ == "__main__":

    path = "/opt/password-manager"
    #path = str(sys.executable)
    #path = path[0:-17]
    #path = "." + path
    checkpath = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
    if not os.path.exists(checkpath):
        # Create a password database for the first time
        Password.create_table()

    if Password._meta.is_auth:
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
