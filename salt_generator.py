from base64 import b64encode
import secrets
import numpy as np
import string


ONLY_NUMBERS = '0123456789'
ONLY_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ONLY_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ONLY_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_NUMBERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PRINTABLE_CHARS = string.printable
RANDOM_STRING_CHARS = PRINTABLE_CHARS.translate(
    {ord(i): None for i in ' \t\n\r\x0b\x0c'})

print(RANDOM_STRING_CHARS)


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
    value, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = np.e if base is None else base
    return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()


def entropy_ideal(length, base=None):
    "Calculates the ideal Shannon entropy of a string with given length"

    prob = 1.0 / length
    base = np.e if base is None else base
    return -1.0 * length * prob * np.log(prob) / np.log(base)


string = ""
num_bytes = 64
random_bytes = secrets.token_bytes(num_bytes)
salt1 = b64encode(random_bytes).decode('utf-8')
salt1 = salt1[0:num_bytes]
salt2 = get_random_string(num_bytes)

print(f"Salt 1: {salt1}")
print(f"Salt 2: {salt2}")

entropy_salt1 = entropy(list(salt1), base=2)
entropy_salt2 = entropy(list(salt2), base=2)
ideal_entropy = entropy_ideal(num_bytes, 2)

print(f"Ideal Shannon entropy: {ideal_entropy}")
print(
    f"Shannon entropy salt 1: {entropy_salt1} - effectiveness: {100*entropy_salt1/ideal_entropy}%")
print(
    f"Shannon entropy salt 2: {entropy_salt2} - effectiveness: {100*entropy_salt2/ideal_entropy}%")
