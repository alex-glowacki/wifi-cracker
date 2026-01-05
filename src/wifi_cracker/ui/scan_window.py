# src/wifi_cracker/ui/scan_window.py

# Standard library
from __future__ import annotations

# Third-party
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
)

# Local application
import wifi_cracker.ui.widgets.buttons as Btn
import wifi_cracker.core.wifi_scan as WifiScan
import wifi_cracker.ui.widgets.text_contents as TextContents

# Classes
class ScanWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan Results")
        self.resize(250, 250)
        
        layout = QVBoxLayout()
        
        scan_btn_text = "Start Scan"
        self.scan_btn = Btn.var_btn(scan_btn_text)
        self.scan_btn.clicked.connect(self._update_scan_results)
        layout.addWidget(self.scan_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Eventually make this a list that will connect to the GUI main window text box.
        ssids = WifiScan.scan_ssids()
        self.scan_results = TextContents.text_content(ssids)
        self.scan_results.setText("\n".join(ssids))
        self.scan_results.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.scan_results)
        
        self.setLayout(layout)
    
    def _update_scan_results(self):
        new_scan_results = WifiScan.scan_ssids()
        self.scan_results.setText("\n".join(new_scan_results))