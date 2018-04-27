
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller.Log import LogTrace
from Controller import ParaSetting

class CharacterDisplayLabel(QLabel):

    def __init__(self):
        LogTrace('CharacterDisplayLabel, Init')
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

    def setBackgroundColor(self, r,g,b):
        LogTrace('CharacterDisplayLabel, setBackgroundColor')
        self.setStyleSheet("background: rgb(%d,%d,%d)"%(r,g,b))

    def setCharacterColor(self, color):
        LogTrace('CharacterDisplayLabel, setCharacterColor')
        pa = QPalette()
        pa.setColor(QPalette.WindowText, color)
        self.setPalette(pa)

    def setFixedHeight(self, height):
        LogTrace('CharacterDisplayLabel, setFixedHeight')
        super(CharacterDisplayLabel, self).setFixedHeight(height)

class ThumbnailListWidget(QListWidget):

    def __init__(self):
        LogTrace('ThumbnailListWidget, Init')
        super(ThumbnailListWidget, self).__init__()
        self.patientName = None

    def setPatientName(self, name):
        LogTrace('ThumbnailListWidget, setPatientName')
        self.patientName = name

    def getPatientName(self):
        LogTrace('ThumbnailListWidget, getPatientName')
        return self.patientName
