# src/wifi_cracker/app.py

# Standard library
import sys

# Third-party
from PyQt6.QtWidgets import QApplication

# Local application
from wifi_cracker.ui.main_window import MainWindow


# Entry point function
def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    return app.exec()