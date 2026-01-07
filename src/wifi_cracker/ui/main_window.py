# src/wifi_cracker/ui/main_window.py

# Standard Library
#from __future__ import annotations
from importlib.metadata import version, PackageNotFoundError
import sys

# Third-party
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QFileDialog,
)

# Local application
import wifi_cracker.ui.widgets.text_boxes as TextBoxes
import wifi_cracker.ui.widgets.buttons as Btn
from wifi_cracker.core.wifi_key_authentication import WifiCracker
from wifi_cracker.ui.scan_window import ScanWindow
from wifi_cracker.ui.crack_window import CrackWindow
from wifi_cracker.ui.widgets.worker import Worker

# Version number with safeguard.
try:
    __version__ = version("wifi-cracker")
except PackageNotFoundError:
    __version__ = "0.1.0-dev"

# Classes
class MainWindow(QMainWindow):
    results_ready = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        
        self.sw = None
        self.cw = None
        self.thread = None
        self.worker = None
        
        self.setWindowTitle(f"wifi_cracker - v{__version__}")
        self.resize(500, 500)
        
        self._create_menu_bar()
        self._setup_ui()
        
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        
        
    def _setup_ui(self):
        # Defining grid layout.
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setRowStretch(3, 1)
        layout.setColumnStretch(3, 1)
        
        # Labels
        layout.addWidget(QLabel("Password Dictionary:"), 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel("Target Network (SSID):"), 1, 0, Qt. AlignmentFlag.AlignLeft)
        
        # Text boxes
        self.password_dictionary_text = TextBoxes.text_box()
        self.ssid_text = TextBoxes.text_box()
        
        layout.addWidget(self.password_dictionary_text, 0, 1)
        layout.addWidget(self.ssid_text, 1, 1)
        
        # Buttons
        self.password_dictionary_btn = Btn.var_btn("BROWSE")
        self.scan_btn = Btn.var_btn("SCAN")
        self.attack_btn = Btn.var_btn("START ATTACK")
        
        self.password_dictionary_btn.clicked.connect(self.open_file_dialog)
        self.scan_btn.clicked.connect(self._show_scan_window)
        self.attack_btn.clicked.connect(self.start_job)
        
        # QSS style sheet coding.
        self.password_dictionary_btn.setObjectName("dictionaryButton")
        self.scan_btn.setObjectName("scanButton")
        self.attack_btn.setObjectName("attackButton")
        
        #self.password_dictionary_btn.setProperty("variant", "primary")
        #self.scan_btn.setProperty("variant", "primary")
        #self.attack_btn.setProperty("variant", "primary")
        
        layout.addWidget(self.password_dictionary_btn, 0, 2)
        layout.addWidget(self.scan_btn, 1, 2)
        layout.addWidget(self.attack_btn, 2, 1)
        
        self.results_window = CrackWindow()
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("File")
        scan_menu = menu_bar.addMenu("Scan")
        
        file_menu.addAction("Open Dictionary").triggered.connect(self.open_file_dialog)
        file_menu.addAction("Exit").triggered.connect(self.close)
        
        scan_menu.addAction("Scan Networks").triggered.connect(self._show_scan_window)
    
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        
        if file_path:
            self.password_dictionary_text.setText(file_path)
    
    
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
        return WifiCracker.crack_dictionary_attack(
            self.ssid_text.text(),
            self.password_dictionary_text.text(),
        )