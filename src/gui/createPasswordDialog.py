import os
import bcrypt
from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from core.utils import *  # Ensure these are defined or imported correctly
import getpass
from playhouse.sqlcipher_ext import SqlCipherDatabase
from core.database import Password


class CreatePasswordDialog(QDialog):
    password_created = pyqtSignal(str)  # Signal to emit when the password is successfully created

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        # Disable resizing, which also disables maximizing
        self.setFixedHeight(100)
        self.setFixedWidth(400)
        self.setWindowTitle("Create master password")

    def initUI(self):
        layout = QFormLayout(self)

        # Create password fields
        self.passwordField = QLineEdit(self)
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.confirmPasswordField = QLineEdit(self)
        self.confirmPasswordField.setEchoMode(QLineEdit.Password)

        # Add fields to layout
        layout.addRow(QLabel("New Password:"), self.passwordField)
        layout.addRow(QLabel("Confirm Password:"), self.confirmPasswordField)

        # Create and connect the button
        self.createButton = QPushButton('Create Password', self)
        self.createButton.clicked.connect(self.createPassword)
        layout.addWidget(self.createButton)

    def createPassword(self):
        password = self.passwordField.text()
        confirm_password = self.confirmPasswordField.text()

        # Check if the passwords match
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "The passwords do not match.")
            return

        # Perform your entropy checks here

        input_entropy = entropy(list(password), 10)
        input_ideal_entropy = entropy_ideal(len(password), 10)
        entropy_ratio = 100*input_entropy/input_ideal_entropy

        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Your password must be at least 8 characters long")
            return
        elif any(i in SPECIAL_CHARS for i in password) == False:
            QMessageBox.warning(self, "Error", "Your password must contain at least one special character.")
            return
        elif any(i in ONLY_LOWERCASE for i in password) == False:
            QMessageBox.warning(self, "Error", "Your password must contain at least one lower-case character.")
            return
        elif any(i in ONLY_UPPERCASE for i in password) == False:
            QMessageBox.warning(self, "Error", "Your password must contain at least one upper-case character.")  
            return      
        elif entropy_ratio < 85:
            QMessageBox.warning(self,"Error", "Your password is too simple.")

        # If all checks pass, hash the password and create the database
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        path = f"/home/{getpass.getuser()}/password-manager"
        try:
            # Write the hashed password to your password file
            # Set up your database
            passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"
            database_path = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
            # Write the hashed password to your password file
            with open(passwd_path, "wb") as f:  # Using "wb" as hashed is bytes
                f.write(hashed)  # hashed is already in bytes, no need to decode
            # Check if the database file already exists to avoid overwriting it
            if not os.path.exists(database_path):
                # Initialize and connect to the database
                db = SqlCipherDatabase(database_path, passphrase=password)  # password should be a string
                # Assuming `Password` is your Peewee model class and it's imported and correctly defined
                Password._meta.database = db
                with db:
                    db.create_tables([Password])  # create_tables expects a list of model classes

            #self.password_created.emit(password)  # Emit the signal with the password
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reject()  # Close the dialog with a reject status

# Rest of your application code
