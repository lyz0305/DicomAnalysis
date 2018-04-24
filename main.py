

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
from scipy.misc import imresize
import qimage2ndarray
from Viewer.DicomBasicContrastViewer import *
from Viewer.DicomViewerTool import *

app = QApplication(sys.argv)
window = DicomViewerTool()
# window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
window.show()
app.exec_()