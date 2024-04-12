from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDockWidget
from svlib.uielem.SvQWidget import SvQWidget
from svlib.abstract.SvError import SvError

class SvDockWidget(QDockWidget):
    """SvDockWidget is a QDockWidget with some predefined parameters"""
    
    def __init__(self, widget:SvQWidget | QWidget, title:str,  parent:QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setParent(parent)
        self.setObjectName(f"SvDockWidget::{str(id(self))}")
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWindowTitle(title)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidget(widget)
        