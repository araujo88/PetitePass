from getpass import getpass

password = "1234"

input = getpass()

if (input == password):
    print("Password correct!")
else:
    print("Password incorrect!")
