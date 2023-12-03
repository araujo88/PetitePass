from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory, QMenu)
from PyQt5.QtCore import Qt
from gui.passwordDialog import PasswordDialog
from gui.generatePasswordDialog import GeneratePasswordDialog
from gui.checkPasswordDialog import CheckPasswordDialog
from gui.updatePasswordDialog import UpdatePasswordDialog
from gui.deletePasswordDialog import DeletePasswordDialog
from gui.modifyMasterPasswordDialog import ModifyMasterPasswordDialog
from core.database import Password

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Password Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Username", "Password", "Created", "Updated"])
        layout.addWidget(self.table)

        # Align the horizontal headers
        for i in range(self.table.columnCount()):
            headerItem = QTableWidgetItem(self.table.horizontalHeaderItem(i).text())
            headerItem.setTextAlignment(Qt.AlignHCenter)
            self.table.setHorizontalHeaderItem(i, headerItem)        

        # Buttons
        # self.addButton = QPushButton('Add Password', self)
        # self.addButton.clicked.connect(self.addPassword)
        # layout.addWidget(self.addButton)

        # self.addButton = QPushButton('Update password', self)
        # self.addButton.clicked.connect(self.updatePassword)
        # layout.addWidget(self.addButton)

        # self.addButton = QPushButton('Delete password', self)
        # self.addButton.clicked.connect(self.deletePassword)
        # layout.addWidget(self.addButton)

        # self.addButton = QPushButton('Generate password', self)
        # self.addButton.clicked.connect(self.generatePassword)
        # layout.addWidget(self.addButton)

        # self.addButton = QPushButton('Check password strength', self)
        # self.addButton.clicked.connect(self.checkPasswordStrength)
        # layout.addWidget(self.addButton)        

        # self.addButton = QPushButton('Modify master password', self)
        # self.addButton.clicked.connect(self.addPassword)
        # layout.addWidget(self.addButton)                  

        # Add other buttons and connect them to respective functions
        # ...
        self.populatePasswordTable()

    def checkPasswordStrength(self):
        checkPasswordDialog = CheckPasswordDialog(self)
        checkPasswordDialog.exec_()  # This will display the dialog


    def addPassword(self):
        dialog = PasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.populatePasswordTable()

    def updatePassword(self):
        dialog = UpdatePasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.populatePasswordTable()

    def deletePassword(self):
        dialog = DeletePasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.populatePasswordTable()                        

    def generatePassword(self):
        dialog = GeneratePasswordDialog(self)
        dialog.exec_()

    def modifyMasterPassword(self):
        dialog = ModifyMasterPasswordDialog(self)
        dialog.exec_()

    def populatePasswordTable(self):
        # Clear existing data
        self.table.clearContents()
        self.table.setRowCount(0)

        # Fetch data from the database
        passwords = Password.select()  # assuming this fetches data from your database
        for row, password in enumerate(passwords):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(password.name))
            self.table.setItem(row, 1, QTableWidgetItem(password.username))
            self.table.setItem(row, 2, QTableWidgetItem(password.password))
            self.table.setItem(row, 3, QTableWidgetItem(str(password.timestamp)))
            self.table.setItem(row, 4, QTableWidgetItem(str(password.updated)))

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        # Create actions
        addAct = contextMenu.addAction("Add password")
        updateAct = contextMenu.addAction("Update password")
        deleteAct = contextMenu.addAction("Delete password")
        generateAct = contextMenu.addAction("Generate password")
        checkAct = contextMenu.addAction("Check password strength")
        modifyMasterAct = contextMenu.addAction("Modify master password")

        # Execute the context menu and get the selected action
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        # Check which action was selected and call the respective method
        if action == addAct:
            self.addPassword()
        elif action == updateAct:
            self.updatePassword()
        elif action == deleteAct:
            self.deletePassword()
        elif action == generateAct:
            self.generatePassword()
        elif action == checkAct:
            self.checkPasswordStrength()
        elif action == modifyMasterAct:
            self.modifyMasterPassword()
