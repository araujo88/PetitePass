from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from core.database import Password
from peewee import DoesNotExist
from datetime import datetime

class UpdatePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Update password entry")

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
        self.buttons = QPushButton('Update', self)
        self.buttons.clicked.connect(self.updatePassword)
        layout.addWidget(self.buttons)

    def updatePassword(self):
        name = self.nameField.text()
        username = self.usernameField.text()
        password = self.passwordField.text()

        try:
            existing_entry = Password.get(Password.name == name)
            if existing_entry is None:
                QMessageBox.warning(self, "Error", "The name does not exist! Please type an existing name for the password.")
            else:
                if username is not None and username != "":
                    existing_entry.username = username
                if password is not None and password != "":
                    existing_entry.password = password
                existing_entry.updated = datetime.now()
                existing_entry.save()
                QMessageBox.information(self, "Success", "Password record updated successfully!")
                self.accept()  
        except DoesNotExist:
                QMessageBox.warning(self, "Error", "The name does not exist! Please type an existing name for the password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reject()
