import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QComboBox, QStyleFactory)
from gui.authDialog import AuthDialog
from gui.mainWindow import MainWindow

class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.authDialog = AuthDialog()
        self.authDialog.login_successful.connect(self.onLoginSuccess)  # Connect the signal
        self.setStyle(QStyleFactory.create("Fusion"))  # Example of setting a style        
        self.initUI()

    def initUI(self):
        if self.authDialog.exec_() == QDialog.Accepted:
            # The actual UI setup is now handled in onLoginSuccess
            pass
        else:
            sys.exit()  # Exit the application if the dialog is closed

    def onLoginSuccess(self):
        self.mainWindow = MainWindow()
        self.setCentralWidget(self.mainWindow)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Password Manager')
        self.show()

    def setupMainWindow(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Password Manager')    
        self.show()


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordManagerApp()
    sys.exit(app.exec_())
