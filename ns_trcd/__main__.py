from PySide2.QtWidgets import QApplication
import pyqtgraph as pg
import sys
from .ui import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())

