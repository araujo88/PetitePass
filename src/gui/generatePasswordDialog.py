from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from PyQt5.QtGui import QIntValidator
from core.utils import generate_password

class GeneratePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        # Disable resizing, which also disables maximizing
        self.setFixedHeight(200)
        self.setFixedWidth(400)      

    def initUI(self):
        layout = QFormLayout(self)
        self.generatedPasswordLabel = QLabel("Generated password:")
        self.generatedPasswordBox = QLineEdit(self)

        # Password Length and Character Set
        self.lengthField = QLineEdit(self)
        self.lengthField.setValidator(QIntValidator(1, 1024))  # Allow only numbers between 1 and 1024
        self.charsetCombo = QComboBox(self)
        self.charsetCombo.addItems(["All printable characters", "All characters except accents", "All letters and numbers", "Only uppercase letters and numbers", "Only uppercase letters", "Only lowercase letters and numbers", "Only lowercase letters", "Only special characters", "Only letters", "Only numbers"])  # Add all options
        layout.addRow(QLabel("Length:"), self.lengthField)
        layout.addRow(QLabel("Character Set:"), self.charsetCombo)

        # Generate Button
        self.generateButton = QPushButton('Generate', self)
        self.generateButton.clicked.connect(self.generatePassword)
        layout.addWidget(self.generateButton)
        layout.addRow(self.generatedPasswordLabel)
        layout.addRow(self.generatedPasswordBox)


    def generatePassword(self):
        try:
            selectedText = self.charsetCombo.currentText()
            self.generatedPasswordBox.setText(generate_password(selectedText, int(self.lengthField.text())))
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Error", str(e))
