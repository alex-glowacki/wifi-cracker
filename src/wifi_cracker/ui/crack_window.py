# src/wifi_cracker/ui/crack_window.py

# Third-party
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

# Local application
from wifi_cracker.ui.constants import (
    CRACK_WINDOW_TITLE,
    CRACK_WINDOW_SIZE,
)


# Classes
class CrackWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle(CRACK_WINDOW_TITLE)
        self.resize(*CRACK_WINDOW_SIZE)
        
        layout = QVBoxLayout(self)
        
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
    
    
    @pyqtSlot(str)
    def append_text(self, text: str) -> None:
        self.log.insertPlainText(text)
        self.log.ensureCursorVisible()