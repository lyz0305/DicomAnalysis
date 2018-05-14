
from Controller.Log import LogClassFuncInfos
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import ParaSetting
class FreeHandROIGUI():

    @LogClassFuncInfos
    def __init__(self):
        self.__layout = None
        self.__btnDraw = None
        self.__btnErase = None

        self.initGUI()

    @LogClassFuncInfos
    def initGUI(self):
        layout = QVBoxLayout()

        label = QLabel()
        label.setStyleSheet('background-color: rgb(%d,%d,%d)' % (ParaSetting.ThumbnailWidgetColorR,
                                                                 ParaSetting.ThumbnailWidgetColorG,
                                                                 ParaSetting.ThumbnailWidgetColorB))
        layout.addWidget(label)

        btnLayout = QVBoxLayout()
        label.setLayout(btnLayout)
        textLabel = QLabel('Free Hand ROI')
        btnDraw = QPushButton('Draw')
        btnErase = QPushButton('Erase')
        btnLayout.addWidget(textLabel)
        btnLayout.addWidget(btnDraw)
        btnLayout.addWidget(btnErase)
        btnLayout.addStretch()

        self.__layout = layout
        self.__btnDraw = btnDraw
        self.__btnErase = btnErase

    @LogClassFuncInfos
    def getLayout(self):
        return self.__layout

    @LogClassFuncInfos
    def connectDraw(self, func):
        self.__btnDraw.clicked.connect(func)

    @LogClassFuncInfos
    def connectErase(self, func):
        self.__btnErase.clicked.connect(func)