from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from core.utils import *
from PyQt5.QtCore import Qt

class CheckPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        # Disable resizing, which also disables maximizing
        self.setFixedHeight(200)
        self.setFixedWidth(400)
        self.setWindowTitle("Check password strength")

    def initUI(self):
        self.passwordLengthLabel=QLabel("Password length:")
        self.shannonEntropyLabel=QLabel("Shannon entropy:")
        self.maxShannonEntropyLabel=QLabel("Maximum Shannon entropy:")
        self.entropyRatioLabel=QLabel("Entropy ratio:")

        layout = QFormLayout(self)

        self.passwordField = QLineEdit(self)
        self.checkButton = QPushButton('Check Password', self)
        self.checkButton.clicked.connect(self.checkPassword)
        layout.addRow(QLabel("Password:"), self.passwordField)
        layout.addWidget(self.checkButton)
        layout.addRow(QLabel())
        layout.addRow(self.passwordLengthLabel)
        layout.addRow(self.shannonEntropyLabel)
        layout.addRow(self.maxShannonEntropyLabel)
        layout.addRow(self.entropyRatioLabel)


    def checkPassword(self):
        password_check = self.passwordField.text()
        if password_check == "":
            QMessageBox.warning(self, "Error", "The password cannot be empty.")
            return
        entropy_check = entropy(list(password_check), 10)
        max_entropy = entropy_ideal(len(password_check), 10)
        ratio = 100*entropy_check/max_entropy
        self.passwordLengthLabel.setText("Password length: " + str(len(password_check)))
        self.shannonEntropyLabel.setText("Shannon entropy: " + str(entropy_check))
        self.maxShannonEntropyLabel.setText("Maximum Shannon entropy: " + str(max_entropy))
        self.entropyRatioLabel.setText("Entropy ratio: " + f"{round(ratio, 2)}%")

        if len(password_check) < 8:
            QMessageBox.warning(self, "Warning", "The length is under 8 characters. The password is weak.")
            return
        elif any(i in SPECIAL_CHARS for i in password_check) == False:
            QMessageBox.warning(self, "Warning", "The password does not contain any special characters. The password is weak.")
            return
        elif any(i in ONLY_LOWERCASE for i in password_check) == False:
            QMessageBox.warning(self, "Warning", "The password does not contain at least one lower-case character. The password is weak.")
            return
        elif any(i in ONLY_UPPERCASE for i in password_check) == False:
            QMessageBox.warning(self, "Warning", "The password does not contain at least one upper-case character. The password is weak.")  
            return      
        elif round(ratio, 2) < 85:
            QMessageBox.warning(self,"Warning", "The password has low entropy. The password is weak")
        else:
            QMessageBox.information(self, "Info", "The password is secure!")

