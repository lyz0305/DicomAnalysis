
from Viewer.DicomBasicContrastViewer import *
from Viewer.DicomBasicPanZoomViewer import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Controller.Log as Log
from Controller.DicomViewerController import *
from Model.DicomViewerModel import *
import os




class DicomToolWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DicomToolWindow, self).__init__(parent)
        Log.LogTrace('DicomToolWindow, Init')
        self.setWindowTitle("DicomTool")
        self.setStyleSheet("background-color:black")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.showMaximized()

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.DicomToolController = DicomToolPageController()
        self.InitModel()
        self.InitGUI()

    def InitModel(self):
        LogTrace('DicomToolWindow, InitModel')
        self.ImageNamesModel = ImageNamesModel()
        self.DicomToolController.SetModel(self.ImageNamesModel)

    def InitGUI(self):
        LogTrace('DicomToolWindow, InitGUI')
        widget = QWidget()
        self.setCentralWidget(widget)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        widget.setLayout(self.layout)
        self.DicomToolController.SetLayout(self.layout)


    def createPanel(self):

        pass


    def createActions(self):
        Log.LogTrace('DicomToolWindow, createActions')
        self.zoomAction = QAction(QIcon('Icons\\Zoom.png'), self.tr("Zoom"), self)
        self.zoomAction.setStatusTip(self.tr("Zoom"))
        self.zoomAction.setCheckable(True)

        self.panAction = QAction(QIcon('Icons\\Pan.png'), self.tr("Pan"), self)
        self.panAction.setStatusTip(self.tr("Pan"))
        self.panAction.setCheckable(True)

        self.contrastAction = QAction(QIcon('Icons\\Contrast.png'),self.tr("Contrast"),self)
        self.contrastAction.setStatusTip(self.tr("Contrast"))
        self.contrastAction.setCheckable(True)


    def createMenus(self):
        Log.LogTrace('DicomToolWindow, createMenus')

    def createToolBars(self):
        Log.LogTrace('DicomToolWindow, createToolBars')
        fileToolBar = self.addToolBar("Print")
        fileToolBar.setStyleSheet("background: rgb(150, 150, 150)")
        fileToolBar.setFixedHeight(50)
        fileToolBar.setIconSize(QSize(50, 50))
        fileToolBar.addAction(self.contrastAction)
        fileToolBar.addAction(self.panAction)
        fileToolBar.addAction(self.zoomAction)
        fileToolBar.addSeparator()

    def dragEnterEvent(self, QEvent ):
        Log.LogTrace('DicomToolWindow, dragEnterEvent')
        # print(QEvent)
        QEvent.acceptProposedAction()
        # QEvent.ignore()


    def dragLeaveEvent(self, QEvent):
        Log.LogTrace('DicomToolWindow, dragLeaveEvent')
        # QEvent.ignore()


    def dragMoveEvent(self, QEvent):
        Log.LogTrace('DicomToolWindow, dragMoveEvent')
        # QEvent.ignore()


    def dragEvent(self, QEvent):
        Log.LogTrace('DicomToolWindow, dragEvent')
        # QEvent.ignore()



    def dropEvent(self, QEvent):
        Log.LogTrace('DicomToolWindow, dropEvent')
        urls = QEvent.mimeData().urls()
        folder = []
        for url in urls:
            folder.append(url.toLocalFile())
        ImageNames = []
        while len(folder) is not 0:

            file = folder[0]
            folder.pop(0)

            if os.path.isdir(file):
                files = os.listdir(file)
                for f in files:
                    folder.append(os.path.join(file,f))
            elif os.path.isfile(file):
                extension = os.path.splitext(file)
                if len(extension[1]) == 0 or extension[1].lower() is '.dcm':
                    ImageNames.append(file)
        self.ImageNamesModel.setImageNames(ImageNames)