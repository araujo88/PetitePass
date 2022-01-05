import string
import numpy as np
from getpass import getpass
import os
import bcrypt
import secrets

is_auth = False

ONLY_NUMBERS = '0123456789'
ONLY_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ONLY_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ONLY_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SPECIAL_CHARS = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'"""
LETTERS_AND_NUMBERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PRINTABLE_CHARS = string.printable
RANDOM_STRING_CHARS = PRINTABLE_CHARS.translate(
    {ord(i): None for i in ' \t\n\r\x0b\x0c'})


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.
    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)
    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def entropy(labels, base=None):
    "Calculates the entropy of a string with given length"
    value, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = np.e if base is None else base
    return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()


def entropy_ideal(length, base=None):
    "Calculates the ideal entropy of a string with given length"
    prob = 1.0 / length
    base = np.e if base is None else base
    return -1.0 * length * prob * np.log(prob) / np.log(base)


if not os.path.isfile('./password'):
    print("Please create a password:")
    while True:
        password_input = getpass()

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
        elif entropy_ratio < 90:
            print("Error: your password is too simple.")
        else:
            break

    password = str.encode(password_input)
    # Hash a password for the first time, with a randomly-generated salt
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    f = open("password", "w")
    # digest = hashlib.sha256(hashed).hexdigest()
    f.write(hashed.decode())
    f.close()
    is_auth = True
else:
    print("Please input your password:")
    password_input = getpass()
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
    print("You are now authenticated.")
    while(True):
        print("\n--------------------------------")
        print("Please input the desired option:")
        print("2 - Check password")
        print("1 - Generate secure password")
        print("0 - Exit")
        print("--------------------------------\n")
        user_input = input()
        if user_input == '1':
            print("Please input the length of the password:")
            length = int(input())
            if length < 8:
                print("Error - a secure password must have at least 8 characters.")
            else:
                secure_password = get_random_string(length)
                print(f"Password generated: {secure_password}")
                secure_password_entropy = entropy(list(secure_password), 2)
                print(f"Entropy: {secure_password_entropy} shannons")
        elif user_input == '2':
            print("Please enter the password to be verified:")
            password_check = getpass()
            entropy_check = entropy(list(password_check), 10)
            max_entropy = entropy_ideal(len(password_check), 10)
            ratio = 100*entropy_check/max_entropy
            print(f"Password length: {len(password_check)}")
            print(f"Shannon entropy: {entropy_check}")
            print(f"Maximum possible Shannon entropy: {max_entropy}")
            print(f"Entropy ratio: {round(ratio, 2)}%")
            if len(password_check) < 8:
                print("The length is under 8 characters. The password is weak.")
            elif any(i in SPECIAL_CHARS for i in password_check) == False:
                print(
                    "The password does not contain any special characters. The password is weak.")
            elif any(i in ONLY_LOWERCASE for i in password_check) == False:
                print(
                    "The password does not contain at least one lower-case character. The password is weak.")
            elif any(i in ONLY_UPPERCASE for i in password_check) == False:
                print(
                    "The password does not contain at least one upper-case character. The password is weak.")
            elif ratio < 90:
                print("The password has low entropy. The password is weak.")
            else:
                print("The password is strong.")
        elif user_input == '0':
            print("Exiting program ...")
            break
        else:
            print("Invalid option.")
