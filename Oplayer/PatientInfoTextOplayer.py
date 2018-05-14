
from Oplayer.BasicOplayer import BasicOplayer
from Controller.Log import LogClassFuncInfos
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Model.DicomViewerModel import DisplayInfoModel, SequenceInfoModel

class PatientInfoTextOplayer(BasicOplayer):

    @LogClassFuncInfos
    def __init__(self, panel):
        super(PatientInfoTextOplayer, self).__init__(panel)
        self.__displayInfoModel = DisplayInfoModel()
        self.__sequenceInfoModel = SequenceInfoModel()

    @LogClassFuncInfos
    def setModel(self, model):

        if model.Name is self.__displayInfoModel.Name:
            self.__displayInfoModel = model
        elif model.Name is self.__sequenceInfoModel.Name:
            self.__sequenceInfoModel = model


    @LogClassFuncInfos
    def paintEvent(self, QPaintEvent):

        height = self.getPanel().height()
        width = self.getPanel().width()

        pos = QPoint(50, height-50)

        painter = QPainter( self.getPanel() )
        painter.setPen(QColor(255, 255, 255))
        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        if len(sequenceInfo.keys()) is 0:
            return
        N = len( sequenceInfo[self.__displayInfoModel.getPatientName()][self.__displayInfoModel.getSeryName()].keys() )
        painter.drawText(pos, '%3d/%3d'%(self.__displayInfoModel.getInstanceNumber(),N))

        pass



