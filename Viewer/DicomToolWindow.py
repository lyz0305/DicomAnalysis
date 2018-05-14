

# from Viewer.DicomBasicViewer import DicomBasicPanZoomViewer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Controller.DicomViewerController import *
from Model.DicomViewerModel import *
import os
from Controller import Log
from Controller import Status


class DicomToolWindow(QMainWindow):

    freeHandROISignal = pyqtSignal(bool)

    @Log.LogClassFuncInfos
    def __init__(self, parent=None):
        super(DicomToolWindow, self).__init__(parent)
        self.setWindowTitle("DicomTool")
        self.setStyleSheet("background-color:black")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.showMaximized()

        self.DicomToolController = DicomToolPageController()
        self.InitModel()
        self.InitGUI()

        self.createActions()
        self.createMenus()
        self.createToolBars()



    @Log.LogClassFuncInfos
    def InitModel(self):
        self.ImageNamesModel = ImageNamesModel()
        self.DicomToolController.setModel(self.ImageNamesModel)

    @Log.LogClassFuncInfos
    def InitGUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        widget.setLayout(self.layout)
        self.DicomToolController.setLayout(self.layout)
        self.freeHandROISignal.connect(self.DicomToolController.freeHandROI)

    @Log.LogClassFuncInfos
    def createPanel(self):
        pass

    @Log.LogClassFuncInfos
    def createActions(self):
        self.zoomAction = QAction(QIcon('Icons\\Zoom.png'), self.tr("Zoom"), self)
        self.zoomAction.setStatusTip(self.tr("Zoom"))
        self.zoomAction.setCheckable(True)
        self.zoomAction.triggered.connect(self.setContrastPanZoom)

        self.panAction = QAction(QIcon('Icons\\Pan.png'), self.tr("Pan"), self)
        self.panAction.setStatusTip(self.tr("Pan"))
        self.panAction.setCheckable(True)
        self.panAction.triggered.connect(self.setContrastPanZoom)

        self.contrastAction = QAction(QIcon('Icons\\Contrast.png'),self.tr("Contrast"),self)
        self.contrastAction.setStatusTip(self.tr("Contrast"))
        self.contrastAction.setCheckable(True)
        self.contrastAction.triggered.connect(self.setContrastPanZoom)

        self.freeHandROIAction = QAction(QIcon('Icons\\FreeHandROI.png'),self.tr("FreeHand"),self)
        self.freeHandROIAction.setStatusTip(self.tr("FreeHandROI"))
        self.freeHandROIAction.setCheckable(True)
        self.freeHandROIAction.setEnabled(False)
        self.freeHandROIAction.triggered.connect(self.freeHandROI)

    @Log.LogClassFuncInfos
    def freeHandROI(self, checked=False):
        self.freeHandROISignal.emit(checked)

    @Log.LogClassFuncInfos
    def setContrastPanZoom(self, checked=False):
        Status.setBTNToNormal()


    @Log.LogClassFuncInfos
    def createMenus(self):
        pass

    @Log.LogClassFuncInfos
    def createToolBars(self):
        fileToolBar = self.addToolBar("Print")
        fileToolBar.setStyleSheet("background: rgb(150, 150, 150)")
        fileToolBar.setFixedHeight(50)
        fileToolBar.setIconSize(QSize(50, 50))
        fileToolBar.addAction(self.contrastAction)
        fileToolBar.addAction(self.panAction)
        fileToolBar.addAction(self.zoomAction)
        fileToolBar.addSeparator()
        fileToolBar.addAction(self.freeHandROIAction)

    @Log.LogClassFuncInfos
    def dragEnterEvent(self, QEvent ):
        # print(QEvent)
        QEvent.acceptProposedAction()
        # QEvent.ignore()

    @Log.LogClassFuncInfos
    def dragLeaveEvent(self, QEvent):
        pass
        # QEvent.ignore()

    @Log.LogClassFuncInfos
    def dragMoveEvent(self, QEvent):
        pass
        # QEvent.ignore()

    @Log.LogClassFuncInfos
    def dragEvent(self, QEvent):
        pass
        # QEvent.ignore()

    @Log.LogClassFuncInfos
    def dropEvent(self, QEvent):
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

        self.freeHandROIAction.setEnabled(True)