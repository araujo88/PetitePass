from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from core.database import Password
from peewee import DoesNotExist

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Form fields
        self.nameField = QLineEdit(self)
        self.usernameField = QLineEdit(self)
        self.passwordField = QLineEdit(self)
        layout.addRow(QLabel("Name:"), self.nameField)
        layout.addRow(QLabel("Username:"), self.usernameField)
        layout.addRow(QLabel("Password:"), self.passwordField)

        # Buttons
        self.buttons = QPushButton('Save', self)
        self.buttons.clicked.connect(self.savePassword)
        layout.addWidget(self.buttons)

    def savePassword(self):
        name = self.nameField.text()
        username = self.usernameField.text()
        password = self.passwordField.text()
        # Call your create_password function here
        try:
            existing_entry = Password.get(Password.name == name)
            if existing_entry is not None:
                QMessageBox.warning(self, "Error", "The name already exists! Please type another name for the password.")
        except DoesNotExist:
                Password.create(name=name, username=username, password=password)
                QMessageBox.information(self, "Success", "Password record created successfully!")
                self.accept()   
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reject()
