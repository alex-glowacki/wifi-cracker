# src/wifi_cracker/ui/widgets/text_contents.py

# Third-party
from PyQt6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QSizePolicy,
)

def text_content(items: list[str]) -> QLabel:
    
    return QLabel("\n".join(items))