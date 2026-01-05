# src/wifi_cracker/ui/crack_window.py

# Third-party
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel,
)

# Local application


# Classes
class CrackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Dictionary Attack")
        self.resize(500, 500)
        
        layout = QVBoxLayout()
        
        self.setLayout(layout)