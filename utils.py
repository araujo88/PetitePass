import string
import numpy as np
import secrets
import os, subprocess
from sys import exit

ONLY_NUMBERS = '0123456789'
ONLY_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ONLY_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ONLY_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NO_ACCENTS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_(){[}]|/?,.!@$#&+%*<=>:;'
SPECIAL_CHARS = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'"""
LETTERS_AND_NUMBERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
LOWERCASE_AND_NUMBERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
UPPERCASE_AND_NUMBERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
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


def generate_password():
    print("Please input the length of the password:")
    length = int(input())
    if length < 1:
        print("Error: invalid length")
    else:
        while(True):
            print("Please input a charset option:")
            print("(9) - All printable characters")
            print("(8) - All characters except accents")
            print("(7) - All letters and numbers")
            print("(6) - Only uppercase letters and numbers")
            print("(5) - Only uppercase letters")
            print("(4) - Only lowercase letters and numbers")
            print("(3) - Only lowercase letters")
            print("(2) - Only special characters")
            print("(1) - Only letters")
            print("(0) - Only numbers")
            user_input = input()

            if user_input == '9':
                char_set = RANDOM_STRING_CHARS
                break
            elif user_input == '8':
                char_set = NO_ACCENTS
                break
            elif user_input == '7':
                char_set = LETTERS_AND_NUMBERS
                break
            elif user_input == '6':
                char_set = UPPERCASE_AND_NUMBERS
                break
            elif user_input == '5':
                char_set = ONLY_UPPERCASE
                break
            elif user_input == '4':
                char_set = LOWERCASE_AND_NUMBERS
                break
            elif user_input == '3':
                char_set = ONLY_LOWERCASE
                break
            elif user_input == '2':
                char_set = SPECIAL_CHARS
                break
            elif user_input == '1':
                char_set = ONLY_LETTERS
                break
            elif user_input == '0':
                char_set = ONLY_NUMBERS
                break
            else:
                print("Invalid option.")

        secure_password = get_random_string(length, allowed_chars=char_set)
        print(f"Password generated: {secure_password}")
        secure_password_entropy = entropy(list(secure_password), 2)
        secure_password_max_entropy = entropy_ideal(length, 2)
        secure_password_ratio = 100*secure_password_entropy/secure_password_max_entropy
        print(f"Entropy: {secure_password_entropy} shannons")
        print(
            f"Maximum possible Shannon entropy: {secure_password_max_entropy}")
        print(f"Entropy ratio: {round(secure_password_ratio, 2)}%")
        if length < 8:
            print("Warning: this password length is under 8 characters!")


def verify_password():
    print("Please enter the password to be verified: ")
    password_check = input()
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
        print("The password does not contain any special characters. The password is weak.")
    elif any(i in ONLY_LOWERCASE for i in password_check) == False:
        print("The password does not contain at least one lower-case character. The password is weak.")
    elif any(i in ONLY_UPPERCASE for i in password_check) == False:
        print("The password does not contain at least one upper-case character. The password is weak.")
    elif ratio < 85:
        print("The password has low entropy. The password is weak.")
    else:
        print("The password is strong.")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        exit("You need to run this script with sudo or as root.")