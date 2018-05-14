

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
import qimage2ndarray
from Viewer.DicomToolWindow import *

import os
if os.path.exists('DicomTool.log'):
    os.remove('DicomTool.log')

app = QApplication(sys.argv)
window = DicomToolWindow()
window.setWindowIcon(QIcon('Icons/D.png'))
window.show()
app.exec_()