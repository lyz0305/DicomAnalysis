
from Oplayer.BasicOplayer import BasicOplayer
from Controller.Log import LogClassFuncInfos
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PatientInfoTextOplayer(BasicOplayer):

    @LogClassFuncInfos
    def __init__(self, painter):
        super(PatientInfoTextOplayer, self).__init__(painter)

    @LogClassFuncInfos
    def QPaintEvent(self, QPaintEvent):
        a = QPoint(50,50)
        self.getPainter().drawText(a,'hello,world\n666')
        self.getPainter().setPen(QColor(255, 255, 255))
        # pa.setColor(QPalette.WindowText, color)
        # self.getPainter().setColor(QPalette.WindowText, Qt.white)
        pass

