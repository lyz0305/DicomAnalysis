
from Viewer.DicomBasicContrastViewer import *
from Viewer.DicomBasicPanZoomViewer import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Controller.Log as Log

class DicomViewerTool(QMainWindow):
    def __init__(self, parent=None):
        super(DicomViewerTool, self).__init__(parent)
        Log.LogTrace('DicomViewerTool, Init')
        self.setWindowTitle("DicomTool")
        self.setStyleSheet("background-color:black")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.showMaximized()

        self.createActions()
        self.createMenus()
        self.createToolBars()

    def createPanel(self):

        pass


    def createActions(self):
        Log.LogTrace('DicomViewerTool, createActions')
        self.zoomAction = QAction(QIcon('Icons\\Zoom.png'), self.tr("Zoom"), self)
        self.zoomAction.setStatusTip(self.tr("Zoom"))

        self.panAction = QAction(QIcon('Icons\\Pan.png'), self.tr("Pan"), self)
        self.panAction.setStatusTip(self.tr("Pan"))

        self.contrastAction = QAction(QIcon('Icons\\Contrast.png'),self.tr("Contrast"),self)
        self.panAction.setStatusTip(self.tr("Contrast"))
        pass

    def createMenus(self):
        Log.LogTrace('DicomViewerTool, createMenus')

    def createToolBars(self):
        Log.LogTrace('DicomViewerTool, createToolBars')
        fileToolBar = self.addToolBar("Print")
        fileToolBar.setStyleSheet("background: rgb(150, 150, 150)")
        fileToolBar.setFixedHeight(50)
        fileToolBar.setIconSize(QSize(50, 50))
        fileToolBar.addAction(self.contrastAction)
        fileToolBar.addAction(self.panAction)
        fileToolBar.addAction(self.zoomAction)
        fileToolBar.addSeparator()

    def dragEnterEvent(self, QEvent ):
        Log.LogTrace('DicomViewerTool, dragEnterEvent')
        # print(QEvent)
        QEvent.acceptProposedAction()
        # QEvent.ignore()
        print('Enter')

    def dragLeaveEvent(self, QEvent):
        Log.LogTrace('DicomViewerTool, dragLeaveEvent')
        # QEvent.ignore()
        print('Leave')

    def dragMoveEvent(self, QEvent):
        Log.LogTrace('DicomViewerTool, dragMoveEvent')
        # QEvent.ignore()
        print('Move')

    def dragEvent(self, QEvent):
        Log.LogTrace('DicomViewerTool, dragEvent')
        # QEvent.ignore()

        print('drag')

    def dropEvent(self, QEvent):
        Log.LogTrace('DicomViewerTool, dropEvent')
        # QEvent.ignore()
        urls = QEvent.mimeData().urls()
        print('drop')