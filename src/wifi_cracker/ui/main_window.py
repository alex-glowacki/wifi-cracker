# src/wifi_cracker/ui/main_window.py

# Standard Library
from __future__ import annotations

# Third-party
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QFileDialog,
)

# Local application
from wifi_cracker.utils.strings import VERSION_NUM

# Classes
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle(f"wifi_cracker - v{VERSION_NUM}")
        self.resize(500, 500)
        self._create_menu_bar()
        
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setRowStretch(3, 1)
        layout.setColumnStretch(3, 1)
        
        self.password_dictionary_label = QLabel("Password Dictionary:")
        layout.addWidget(self.password_dictionary_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
           
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("File")
        open_dictionary_menu = file_menu.addAction("Open Dictionary")
        exit_action = file_menu.addAction("Exit")
        
        open_dictionary_menu.triggered.connect(self.open_file_dialog)
        exit_action.triggered.connect(self.close)
    
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        
        if file_path:
            pass
        