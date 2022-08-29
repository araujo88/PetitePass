# password-manager

A lightweight terminal-based password manager coded with Python using SQLCipher for SQLite database encryption.

## Screenshot

![screenshot](Screenshot.png)

## Getting started

`make install-requirements` <br>
`make build` <br>
`sudo make install` <br>

When running for the first time, run with `sudo`:

`sudo password-manager`

## Pre-requisites:

Python 3.10

## Building

### Install virtualenv

`pip3 install virtualenv`

### Create virtual environment

`virtualenv env`

### Activate virtual environment

`source env/bin/activate`

### Install requirements

`pip3 install -r requirements.txt`

### Generate binary

`pyinstaller --onefile --paths=/env/Lib/site-packages password-manager.py`

## Running

`dist/password-manager`

## Usage

At first run, the program will request a password creation for managing the password database. This password must satisfy certain requirements and be entered twice. THIS PASSWORD CANNOT BE RECOVERED WITHOUT RESETTING THE DATABASE.

When the password is created, two files should have been created. One stores the password salt (5f4dcc3b5aa765d61d8327deb882cf99) and the other file (48cccca3bab2ad18832233ee8dff1b0b.db) stores the password encrypted database itself. IF THESE FILES ARE DELETED, ALL STORED DATA WILL BE LOST. The user can upload these files, along with the binary, in a cloud service, although this is highly discouraged. To achieve the most security, all data must be kept offline.

When the user is logged in, the following options are available:

`--------------------------------` <br />
`Please input the desired option:` <br />
` ` <br />
`(6) - List registered passwords` <br />
`(5) - Register a new password record` <br />
`(4) - Update a password record` <br />
`(3) - Delete a password record` <br />
`(2) - Check password security` <br />
`(1) - Generate secure password` <br />
`(0) - Exit` <br />
`--------------------------------` <br />

Option 6 will print all registered passwords in the database, including their identification name, the username (if applicable) the password itself, the data of creation and the data of the last update.

Option 5 will request the user data for a new input in the database. The field "Username" is optional. The data of creation is generated automatically.

Option 4 enables the user to update a database entry by its identification name.

Option 3 enables the user to delete a database entry by its identification name.

Option 2 analyzes a password (string) entered by the user and outputs Shannon entropy, maximum possible Shannon entropy and analyzes password safety guidelines in general.

Option 1 generates a secure password given an input length by the user and a charset.

Option 0 exits the program.
