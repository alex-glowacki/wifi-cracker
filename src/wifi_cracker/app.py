# src/wifi_cracker/app.py

# Standard library
import sys

# Third-party
from PyQt6.QtWidgets import QApplication

# Local application
from ui.main_window import MainWindow


# Entry point function
def main() -> int:
    """
    Application startup logic.
    Creates the QApplication and main window.
    """
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    return app.exec()