# src/wifi_cracker/ui/widgets/buttons.py

# Third-party
from PyQt6.QtWidgets import QPushButton

def var_btn(text):
    btn = QPushButton(f"{text}")
    btn.setMaximumHeight(25)
    btn.setMinimumWidth(50)
    
    return btn