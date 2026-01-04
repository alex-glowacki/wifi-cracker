# src/wifi_cracker/ui/main_window.py

# Third-party
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

# Local application
from utils.strings import VERSION_NUM

# Classes
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle(f"wifi_cracker - v{VERSION_NUM}")
        self.resize(500, 500)
        
        layout = QVBoxLayout()
        
        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
        