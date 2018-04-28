
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import Log
from Controller import ParaSetting
from Viewer import DicomViewViewer

class CharacterDisplayLabel(QLabel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(CharacterDisplayLabel,self).__init__()
        ft = QFont()
        ft.setPointSize(12)
        self.setFont(ft)
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(ParaSetting.ThumbnailPatientNameHeight)
        self.setFixedWidth(ParaSetting.ThumbnailWidgetWidth)

    @Log.LogClassFuncInfos
    def setBackgroundColor(self, r,g,b,a):
        self.setStyleSheet("background: rgb(%d,%d,%d,%d)"%(r,g,b,a))

    @Log.LogClassFuncInfos
    def setCharacterColor(self, color):
        pa = QPalette()
        pa.setColor(QPalette.WindowText, color)
        self.setPalette(pa)

    @Log.LogClassFuncInfos
    def setFixedHeight(self, height):
        super(CharacterDisplayLabel, self).setFixedHeight(height)

class ThumbnailListWidget(QListWidget):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(ThumbnailListWidget, self).__init__()
        self.patientName = None

    @Log.LogClassFuncInfos
    def setPatientName(self, name):
        self.patientName = name

    @Log.LogClassFuncInfos
    def getPatientName(self):
        return self.patientName

    @Log.LogClassFuncInfos
    def setAllToNotSelected(self):
        N = self.count()
        for i in range(N):
            widgetItem = self.item(i)
            widget = self.itemWidget(widgetItem)
            if isinstance(widget,
                          DicomViewViewer.ThumbnailViewer):
                widget.setSelectState(False)