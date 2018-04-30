
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
        self.__property = dict()

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

    @Log.LogClassFuncInfos
    def setProperty(self, name, val):
        self.__property[name] = val

    @Log.LogClassFuncInfos
    def getProperty(self, name):
        if name in self.__property.keys():
            return self.__property[name]
        else:
            return None

# class ThumbnailListWidget(QListWidget):
#
#     @Log.LogClassFuncInfos
#     def __init__(self):
#         super(ThumbnailListWidget, self).__init__()
#         self.__patientName = None
#
#     @Log.LogClassFuncInfos
#     def setPatientName(self, name):
#         self.__patientName = name
#
#     @Log.LogClassFuncInfos
#     def getPatientName(self):
#         return self.__patientName
#
#     @Log.LogClassFuncInfos
#     def setAllToNotSelected(self):
#         N = self.count()
#         for i in range(N):
#             widgetItem = self.item(i)
#             widget = self.itemWidget(widgetItem)
#             if isinstance(widget,
#                           DicomViewViewer.ThumbnailViewer):
#                 widget.setSelectState(False)