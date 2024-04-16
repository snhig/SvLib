from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class SvQWidget(QWidget):
    """SvQWidget is a QWidget with some predefined methods"""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setObjectName(f"SvQWidget::{str(id(self))}")