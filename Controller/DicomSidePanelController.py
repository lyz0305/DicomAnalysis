
from Controller.Observe import *
from Controller.DicomBaseController import *
from Model.DicomViewerModel import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import ParaSetting
from Controller import Log
from Viewer.SidePanelGUI import FreeHandROIGUI
from Controller import Status

class DicomSidePanelController(DicomBaseController, Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomSidePanelController, self).__init__
        self.__label = QLabel()
        self.__layout = QVBoxLayout()
        self.__label.setLayout(self.__layout)
        self.__label.setMaximumWidth(ParaSetting.SidePanelWidth)
        self.__label.setStyleSheet('background-color: rgb(%d,%d,%d)' % (ParaSetting.ThumbnailWidgetColorR,
                                                                        ParaSetting.ThumbnailWidgetColorG,
                                                                        ParaSetting.ThumbnailWidgetColorB))
        self.__label.hide()

        self.__sidePanel = None
        self.__closeBtn = QPushButton('Close')

    @Log.LogClassFuncInfos
    def initGUI(self):
        pass

    @Log.LogClassFuncInfos
    def hide(self):
        self.__label.hide()

    @Log.LogClassFuncInfos
    def initFreeHandROIGUI(self):

        if self.__sidePanel is None:

            freeHandROIGUI = FreeHandROIGUI()
            self.__layout.addLayout( freeHandROIGUI.getLayout() )
            self.__sidePanel = freeHandROIGUI
            freeHandROIGUI.connectDraw(self.setBTNStatusToFreeHandROIDraw)
            freeHandROIGUI.connectErase(self.setBTNStatusToFreeHandROIErase)

            self.addCloseBtn()

        # elif self.__sidePanel is not None and self.__sidePanel.Name is
        self.__label.show()

    @Log.LogClassFuncInfos
    def addCloseBtn(self):
        self.__layout.addStretch()
        self.__layout.addWidget(self.__closeBtn)
        self.__closeBtn.clicked.connect(self.sidePanelClose)

    @Log.LogClassFuncInfos
    def sidePanelClose(self, checked=False):
        self.__label.hide()

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        layout.addWidget(self.__label)

    @Log.LogClassFuncInfos
    def setBTNStatusToFreeHandROIDraw(self, checked=False):
        Status.setBTNToFreeHandROIDraw()

    @Log.LogClassFuncInfos
    def setBTNStatusToFreeHandROIErase(self, checked=False):
        Status.setBTNToFreeHandROIErase()