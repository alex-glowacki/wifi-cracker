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
import wifi_cracker.ui.widgets.text_boxes as TextBoxes
import wifi_cracker.ui.widgets.buttons as Btn
from wifi_cracker.core.wifi_key_authentication import WifiCracker
from wifi_cracker.ui.scan_window import ScanWindow
from wifi_cracker.ui.crack_window import CrackWindow

# Classes
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.sw = None
        self.cw = None
        self.setWindowTitle(f"wifi_cracker - v{VERSION_NUM}")
        self.resize(500, 500)
        self._create_menu_bar()
        
        
        # Defining grid layout.
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setRowStretch(3, 1)
        layout.setColumnStretch(3, 1)
        
        
        # Labels.
        self.password_dictionary_label = QLabel("Password Dictionary:")
        layout.addWidget(self.password_dictionary_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.ssid_label = QLabel("Target Network (SSID):")
        layout.addWidget(self.ssid_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        
        
        # Text boxes.
        self.password_dictionary_text = TextBoxes.text_box()
        layout.addWidget(self.password_dictionary_text, 0, 1, Qt.AlignmentFlag.AlignLeft)
        
        self.ssid_text = TextBoxes.text_box()
        layout.addWidget(self.ssid_text, 1, 1, Qt.AlignmentFlag.AlignLeft)
        
        
        # Buttons.
        password_btn_text = "Browse"
        self.password_dictionary_btn = Btn.var_btn(password_btn_text)
        self.password_dictionary_btn.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.password_dictionary_btn, 0, 2, Qt.AlignmentFlag.AlignLeft)
        
        scan_btn_text = "Scan"
        self.scan_btn = Btn.var_btn(scan_btn_text)
        self.scan_btn.clicked.connect(self._show_scan_window)
        layout.addWidget(self.scan_btn, 1, 2, Qt.AlignmentFlag.AlignLeft)
        
        crack_btn_text = "Start Attack"
        self.crack_btn = Btn.var_btn(crack_btn_text)
        self.cracker = WifiCracker()
        #self.crack_btn.clicked.connect(self._show_crack_window)
        self.crack_btn.clicked.connect(self._crack_wifi)
        layout.addWidget(self.crack_btn, 2, 1, Qt.AlignmentFlag.AlignLeft)
        
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
           
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Options available under "File".
        file_menu = menu_bar.addMenu("File")
        open_dictionary_menu = file_menu.addAction("Open Dictionary")
        exit_action = file_menu.addAction("Exit")
        
        # Options available under "Scan".
        scan_menu = menu_bar.addMenu("Scan")
        scan_action = scan_menu.addAction("Scan Networks")
        
        # Linking available options.
        open_dictionary_menu.triggered.connect(self.open_file_dialog)
        exit_action.triggered.connect(self.close)
        #scan_action.triggered.connect(WifiScan.main)
        scan_action.triggered.connect(self._show_scan_window)
    
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        
        if file_path:
            self.password_dictionary_text.setText(file_path)
            pass
    
    
    def _show_scan_window(self):
        if self.sw is None:
            self.sw = ScanWindow()
        self.sw.show()


    def _show_crack_window(self):
        if self.cw is None:
            self.cw = CrackWindow()
        self.cw.show()
    
    
    def _crack_wifi(self):
        self.cracker.crack_dictionary_attack(
            self.ssid_text.text().strip(),
            self.password_dictionary_text.text().strip()
        )