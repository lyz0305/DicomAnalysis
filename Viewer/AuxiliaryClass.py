
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller.Log import LogTrace

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
        self.setFixedHeight(60)
        self.setAlignment(Qt.AlignCenter)

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