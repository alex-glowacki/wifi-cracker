# src/wifi_cracker/app.py

# Standard library
import sys

# Third-party
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Local application
from wifi_cracker.ui.main_window import MainWindow


# Entry point function
def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    
    qss_path = Path(__file__).resolve().parent / "ui" / "style.qss"
    app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    
    window = MainWindow()
    window.show()
    
    return app.exec()