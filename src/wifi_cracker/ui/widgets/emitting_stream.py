# src/wifi_cracker/ui/widgets/emitting_stream.py

# Third-party
from PyQt6.QtCore import (
    QObject,
)


# Classes
class EmittingStream(QObject):
    def __init__(self, emit_fn):
        self._emit = emit_fn
        
    
    def write(self, text):
        if text:
            self._emit(text)
        
    
    def flush(self):
        pass  # Needed for initialization.