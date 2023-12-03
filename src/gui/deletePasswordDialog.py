from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from core.database import Password
from peewee import DoesNotExist

class DeletePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Delete password entry")

    def initUI(self):
        layout = QFormLayout(self)

        # Form fields
        self.nameField = QLineEdit(self)
        layout.addRow(QLabel("Name:"), self.nameField)

        # Buttons
        self.buttons = QPushButton('Delete', self)
        self.buttons.clicked.connect(self.deletePassword)
        layout.addWidget(self.buttons)

    def deletePassword(self):
        name = self.nameField.text()

        try:
            existing_entry = Password.get(Password.name == name)
            if existing_entry is None:
                QMessageBox.warning(self, "Error", "The name does not exist! Please type an existing name for the password.")
            else:
                existing_entry.delete_instance()
                QMessageBox.information(self, "Success", "Password record deleted successfully!")
                self.accept()  
        except DoesNotExist:
                QMessageBox.warning(self, "Error", "The name does not exist! Please type an existing name for the password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reject()
