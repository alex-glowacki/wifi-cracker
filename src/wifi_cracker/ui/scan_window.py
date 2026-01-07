# src/wifi_cracker/ui/scan_window.py

# Standard library
from __future__ import annotations

# Third-party
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget


# Local application
import wifi_cracker.core.wifi_scan as WifiScan
import wifi_cracker.ui.widgets.buttons as Btn
import wifi_cracker.ui.widgets.text_contents as TextContents
from wifi_cracker.ui.constants import (
    SCAN_WINDOW_TITLE,
    SCAN_WINDOW_SIZE,
    SCAN_BUTTON_TEXT,
)


# Classes
class ScanWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle(SCAN_WINDOW_TITLE)
        self.resize(*SCAN_WINDOW_SIZE)
        
        layout = QVBoxLayout()
        
        self.scan_btn = Btn.var_btn(SCAN_BUTTON_TEXT)
        self.scan_btn.clicked.connect(self._update_scan_results)
        layout.addWidget(self.scan_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        ssids = WifiScan.scan_ssids()
        
        self.scan_results = TextContents.text_content(ssids)
        self.scan_results.setText("\n".join(ssids))
        self.scan_results.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        
        layout.addWidget(self.scan_results)
        self.setLayout(layout)
        
    
    def _update_scan_results(self) -> None:
        ssids = WifiScan.scan_ssids()
        self.scan_results.setText("\n".join(ssids))