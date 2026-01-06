# src/wifi_cracker/ui/crack_window.py

# Third-party
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
)
from PyQt6.QtCore import (
    pyqtSlot,
)


# Classes
class CrackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Dictionary Attack")
        self.resize(500, 500)
        
        layout = QVBoxLayout(self)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
    
    
    @pyqtSlot(str)
    def append_text(self, text: str):
        self.log.insertPlainText(text)
        self.log.ensureCursorVisible()