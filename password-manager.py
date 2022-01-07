import os
from utils import *
from playhouse.sqlcipher_ext import *
from database import *

if __name__ == "__main__":

    if not os.path.isfile('./passwords.db'):
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
