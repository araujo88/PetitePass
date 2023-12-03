from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
import getpass
import os
import bcrypt
from playhouse.sqlcipher_ext import SqlCipherDatabase
from gui.createPasswordDialog import CreatePasswordDialog
from core.database import Password

class AuthDialog(QDialog):
    login_successful = pyqtSignal()  # Signal to indicate successful login

    def __init__(self):
        super().__init__()
        self.initUI()
        # Disable resizing, which also disables maximizing
        self.setFixedHeight(80)
        self.setFixedWidth(400)
        self.setWindowTitle("Login")

    def initUI(self):
        # Layout and form elements
        layout = QFormLayout(self)
        self.passwordField = QLineEdit(self)
        self.passwordField.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel("Password:"), self.passwordField)
        self.buttons = QPushButton('Login', self)
        self.buttons.clicked.connect(self.handleLogin)
        layout.addWidget(self.buttons)
        path = f"/home/{getpass.getuser()}/password-manager"
        if not os.path.exists(path):
            os.makedirs(path)        
        checkpath = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
        passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"

        if not os.path.exists(checkpath):
            QMessageBox.information(self, "Database does not exist", "Please, create a new password for the database.")
            self.handleNewPasswordCreation(checkpath, passwd_path)        

    def handleLogin(self):
        path = f"/home/{getpass.getuser()}/password-manager"
        checkpath = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
        passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"

        self.authenticateUser(checkpath, passwd_path)

    def handleNewPasswordCreation(self, checkpath, passwd_path):
        createPasswordDialog = CreatePasswordDialog(self)
        if createPasswordDialog.exec_() == QDialog.Accepted:
            # The password was successfully created
            # You can now use the created password to set up your database etc.
            QMessageBox.information(self, "Success", "Password was successfully created.")
            self.login_successful.emit()  # Emit the login successful signal
        else:
            # The user cancelled or there was an error
            QMessageBox.warning(self, "Error", "Password creation was cancelled or failed.")

    def authenticateUser(self, checkpath, passwd_path):
        path = f"/home/{getpass.getuser()}/password-manager"        
        password_input = self.passwordField.text()
        password = str.encode(password_input)
        passwd_path = path + "/5f4dcc3b5aa765d61d8327deb882cf99"
        f = open(passwd_path)
        hashed = str.encode(f.readline())
        if bcrypt.checkpw(password, hashed):
            QMessageBox.information(self, "Success", "The password entered is correct.")
            database_path = path + "/48cccca3bab2ad18832233ee8dff1b0b.db"
            global db
            db = SqlCipherDatabase(
                database_path, passphrase=password_input)
            Password._meta.database = db
            is_auth = True
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            is_auth = False
            return

        if is_auth:
            self.login_successful.emit()
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            return

