# src/wifi_cracker/ui/widgets/worker.py

# Standard library
import contextlib
import traceback

# Third-party
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
)

# Local application
from wifi_cracker.ui.widgets.emitting_stream import EmittingStream


# Classes
class Worker(QObject):
    output = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal()
    
    
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        
    
    @pyqtSlot()
    def run(self):
        try:
            out_stream = EmittingStream(self.output.emit)
            err_stream = EmittingStream(self.output.emit)

            with contextlib.redirect_stdout(out_stream), contextlib.redirect_stderr(err_stream):
                self.fn(*self.args, **self.kwargs)
            
        except Exception:
            self.error.emit(traceback.format_exc())
        finally:
            self.finished.emit()