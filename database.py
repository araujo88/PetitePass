import datetime
import getpass
import os

from playhouse.sqlcipher_ext import *


class Password(Model):
    name = TextField()
    password = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        if not os.path.isfile('./passwords.db'):
            password = getpass.getpass('Please create the database password: ')
        else:
            password = getpass.getpass('Enter the database password: ')
        db = SqlCipherDatabase('passwords.db', passphrase=password)
        database = db


def create_password():
    try:
        print("Input the password identification name:")
        input_name = input()
        print("Input the matching password:")
        input_password = input()
        Password.create(name=input_name, password=input_password)
    except:
        print("An error occurred.")
    finally:
        print("Password record created successfully!")


def print_passwords():
    try:
        print("Registered passwords:\n")
        for password in Password.select():
            print(
                f"Name: {password.name} | Password: {password.password} | Created: {password.timestamp}")
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
        password.save()
    except:
        print("An error occurred.")
    finally:
        print("Password updated successfully!")


def delete_password():
    try:
        print("Input the password identification name to be deleted:")
        input_name = input()
        password = Password.get(Password.name == input_name)
        password.delete_instance()
    except:
        print("An error occurred.")
    finally:
        print("Record deleted successfully!")
