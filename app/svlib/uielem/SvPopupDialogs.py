from PySide6.QtWidgets import QPushButton, QMessageBox, QFileDialog, QApplication
from PySide6.QtGui import QAction, QIcon, QDesktopServices
from PySide6.QtCore import Qt
import sys
__RESOURCE_HELP_LINK__ = "www.google.com"

def open_manual():
    QDesktopServices.openUrl(__RESOURCE_HELP_LINK__)
LAB_SAFETY_TEXT = "\n\nPlease continue to the 'User Manual / Safety Guide' for more information."
PHONES_TEXT = "\n\nLab Manager: Thomas Masterson (650) 436-8934\nLab Manager Alt.: David Steele (510) 846-3243"
def quit_application():
    QApplication.instance().quit()

def setResourceHelpLink(url:str):
    global __RESOURCE_HELP_LINK__
    __RESOURCE_HELP_LINK__ = url

class AbstractMessageBox(QMessageBox):
    def __init__(self, parent, message="Error", title="Error", block_input=True):
        super().__init__(parent=parent)
        self.setWindowTitle(f"{title}")
        self.setText(f"{message}")
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Open)
        self.setButtonText(QMessageBox.Open, "User Manual / Safety Guide")
        self.open_action = self.button(QMessageBox.Open)
        self.open_action.clicked.connect(open_manual)
        
        self.addButton(QMessageBox.Abort)
        self.setButtonText(QMessageBox.Abort, "Quit Application")
        self.quit_action = self.button(QMessageBox.Abort)
        self.quit_action.clicked.connect(quit_application)
        
        if not block_input:
            self.setWindowModality(Qt.WindowModality.WindowModal)


class Critical(QMessageBox):
    def __init__(self,parent, message="Error", title="Critical", block_input=True):
        super().__init__(parent=parent, icon=QMessageBox.Critical)
        self.setWindowTitle(f"{title}")
        self.setText(f"{message} {LAB_SAFETY_TEXT}")
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Open)
        self.setButtonText(QMessageBox.Open, "User Manual / Safety Guide")
        self.open_action = self.button(QMessageBox.Open)
        self.open_action.clicked.connect(open_manual)
        
        self.addButton(QMessageBox.Abort)
        self.setButtonText(QMessageBox.Abort, "Quit Application")
        self.quit_action = self.button(QMessageBox.Abort)
        self.quit_action.clicked.connect(quit_application)
        
        if not block_input:
            self.setWindowModality(Qt.WindowModality.WindowModal)
    
        
class Information(QMessageBox):
    def __init__(self,parent, message="Info", title="Info", block_input=False):
        super().__init__(parent=parent, icon=QMessageBox.Information)
        self.setWindowTitle(f"{title}")
        self.setText(f"{message} {LAB_SAFETY_TEXT}")
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Open)
        self.setButtonText(QMessageBox.Open, "User Manual / Safety Guide")
        self.open_action = self.button(QMessageBox.Open)
        self.open_action.clicked.connect(open_manual)
        if not block_input:
            self.setWindowModality(Qt.WindowModality.WindowModal)
        

class Warning(QMessageBox):
    def __init__(self,parent,  message="Warning", title="Warning", block_input=True):
        super().__init__(parent=parent, icon=QMessageBox.Warning)
        self.setWindowTitle(f"{title}")
        self.setText(f"{message} {LAB_SAFETY_TEXT}")
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Open)
        self.setButtonText(QMessageBox.Open, "User Manual / Safety Guide")
        self.open_action = self.button(QMessageBox.Open)
        self.open_action.clicked.connect(open_manual)
        
        self.addButton(QMessageBox.Abort)
        self.setButtonText(QMessageBox.Abort, "Quit Application")
        self.quit_action = self.button(QMessageBox.Abort)
        self.quit_action.clicked.connect(quit_application)
        
        if not block_input:
            self.setWindowModality(Qt.WindowModality.WindowModal)
        

