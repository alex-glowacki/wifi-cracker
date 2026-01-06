# src/wifi_cracker/ui/main_window.py

# Standard Library
from __future__ import annotations
import sys

# Third-party
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QThread,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
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
from wifi_cracker.ui.widgets.worker import Worker



# Classes
class MainWindow(QMainWindow):
    results_ready = pyqtSignal(str)
    
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
        # Password Dictionary label definition.
        self.password_dictionary_label = QLabel("Password Dictionary:")
        layout.addWidget(self.password_dictionary_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        
        # SSID label definition.
        self.ssid_label = QLabel("Target Network (SSID):")
        layout.addWidget(self.ssid_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        
        
        # Text boxes.
        # Password dictionary text file input box.
        self.password_dictionary_text = TextBoxes.text_box()
        layout.addWidget(self.password_dictionary_text, 0, 1, Qt.AlignmentFlag.AlignLeft)
        
        # SSID input text box.
        self.ssid_text = TextBoxes.text_box()
        layout.addWidget(self.ssid_text, 1, 1, Qt.AlignmentFlag.AlignLeft)
        
        
        # Buttons.
        # Browse button definition.
        password_btn_text = "Browse"
        self.password_dictionary_btn = Btn.var_btn(password_btn_text)
        self.password_dictionary_btn.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.password_dictionary_btn, 0, 2, Qt.AlignmentFlag.AlignLeft)
        
        # Scan button definition.
        scan_btn_text = "Scan"
        self.scan_btn = Btn.var_btn(scan_btn_text)
        self.scan_btn.clicked.connect(self._show_scan_window)
        layout.addWidget(self.scan_btn, 1, 2, Qt.AlignmentFlag.AlignLeft)
        
        # Start Attack button definition.
        attack_btn_text = "Start Attack"
        self.attack_btn = Btn.var_btn(attack_btn_text)
        self.attack_btn.clicked.connect(self.start_job)
        layout.addWidget(self.attack_btn, 2, 1, Qt.AlignmentFlag.AlignLeft)
        
        self.results_window = CrackWindow()
        
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        
        
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
    
    
    def start_job(self):
        self.results_window.show()
        
        # Create stream and connect it to the results window.
        self.thread = QThread()
        self.worker = Worker(self._attack)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.output.connect(self.results_window.append_text)
        self.worker.error.connect(self.results_window.append_text)
        self.worker.finished.connect(self.thread.quit)
        
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()
    
    
    def _attack(self):
        ssid_text = self.ssid_text.text()
        password_text = self.password_dictionary_text.text()
        
        return WifiCracker.crack_dictionary_attack(ssid_text, password_text)