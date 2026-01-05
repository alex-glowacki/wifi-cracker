# src/wifi_cracker/ui/widgets/text_boxes.py

# Third-party
from PyQt6.QtWidgets import QLineEdit

def text_box():
    name_box = QLineEdit()
    name_box.setMaximumHeight(25)
    name_box.setMinimumWidth(250)
    
    return name_box