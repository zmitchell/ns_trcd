from PySide2.QtWidgets import QApplication
import sys
from .oscilloscope import Oscilloscope
from .ui import MainWindow


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# sys.exit(app.exec_())

scope = Oscilloscope()
