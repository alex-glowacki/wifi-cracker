# src/wifi_cracker/ui/main_window.py

# Third-party
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

# Classes
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("wifi_cracker")
        self.resize(500, 500)
        
        layout = QVBoxLayout()
        
        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
        