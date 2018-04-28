
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
from scipy.misc import imresize
import qimage2ndarray
import Viewer.EventDecision as Event
import Controller.Log as Log
from Controller import Log
import Controller.ParaSetting as Setting


class DicomBasicContrastViewer(QLabel):

    @Log.LogClassFuncInfos
    def __init__(self,parent=None):
        super(DicomBasicContrastViewer,self).__init__(parent)
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)
        self.ContrastAble = True
        self.originalImg = None
        self.displayImg = None
        self.setMinimumSize(1,1)
        self.pressPoint = [-1,-1]
        self.releasePoint = [-1,-1]
        self.currentPoint = [-1,-1]
        self.oldPoint = [-1,-1]

        self.contrast = dict()
        self.contrast['center'] = -9999
        self.contrast['width'] = -9999

    @Log.LogClassFuncInfos
    def SetContrastAble(self, able):
        self.ContrastAble = able

    @Log.LogClassFuncInfos
    def setContrast(self,center,width):
        self.contrast['center'] = center
        self.contrast['width'] = width
        self.updateViewer()

    @Log.LogClassFuncInfos
    def setImage(self,image):
        self.originalImg = image
        self.updateImgSize()
        self.resetcontrast()

    @Log.LogClassFuncInfos
    def resetcontrast(self):
        MIN = self.displayImg.min()
        MAX = self.displayImg.max()
        center = (MIN + MAX) / 2
        width = (MAX - MIN)
        self.setContrast(center=center, width=width)

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        self.updateImgSize()

    @Log.LogClassFuncInfos
    def updateImgSize(self):
        if self.originalImg is None:
            return
        size = [self.height(), self.width()]
        zoomImg = imresize(self.originalImg, [int(size[0]), int(size[1])], 'lanczos', mode='I')
        self.displayImg = zoomImg
        self.updateViewer()

    @Log.LogClassFuncInfos
    def updateViewer(self):
        if self.displayImg is None:
            return
        MIN = (2*self.contrast['center'] - self.contrast['width'])/2.0 + 0.5
        MAX = (2*self.contrast['center'] + self.contrast['width'])/2.0 + 0.5
        dFactor = 255.0/(MAX-MIN)
        disImg = (self.displayImg - MIN)*dFactor
        # disImg = (self.originalImg - MIN)*dFactor
        disImg[disImg<0] = 0
        disImg[disImg>255] = 255
        QImg = qimage2ndarray.gray2qimage(disImg)
        self.setPixmap(QPixmap.fromImage(QImg))

    @Log.LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        scenePos = QMouseEvent.pos()
        self.pressPoint = [scenePos.x(), scenePos.y()]
        self.oldPoint = [scenePos.x(), scenePos.y()]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.releasePoint = [pos.x(), pos.y()]
        self.pressPoint = [-1,-1]

        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.currentPoint = [pos.x(), pos.y()]
        if self.pressPoint[0] is not -1 and self.pressPoint[1] is not -1:
            if self.ContrastAble and Event.MouseMoveEvent(QMouseEvent) == Event.Contrast:
                dx = self.currentPoint[0] - self.oldPoint[0]
                dy = self.currentPoint[1] - self.oldPoint[1]
                self.setContrast(center=self.contrast['center'] + dx*Setting.contrastRatio,
                                 width=self.contrast['width'] + dy*Setting.contrastRatio)


        self.oldPoint = [pos.x(), pos.y()]
        QMouseEvent.ignore()

        # print([pos.x(), pos.y()])

if __name__ == '__main__':

    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setWindowTitle("QDicomLabel Test")
            self.resize(500,500)






            widget = QWidget()
            widget.setStyleSheet("background-color:black")
            self.setCentralWidget(widget)
            layout = QHBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            widget.setLayout(layout)


            listWidget = QListWidget()
            listWidget.setFixedWidth(200)
            listWidget.setStyleSheet("background: rgb(150, 150, 150)")

            testWidget = QWidget()
            testWidget.setStyleSheet("background: rgb(250, 250, 150)")
            layout.addWidget(testWidget)
            # layout.addWidget(listWidget)
            # layout.addStretch()

            image_widget = QWidget()
            # layout.addWidget(image_widget)


            # self.setMouseTracking(True)
            self.imagelabel = DicomBasicContrastViewer()
            self.imagelabel.setParent(image_widget)
            #
            # # self.imagelabel.show()
            # width = self.imagelabel.width()
            # height = self.imagelabel.height()
            self.imagelabel.setGeometry(100, 20,  320,  320)

            # layout.addWidget(widget)

            # layout = QHBoxLayout()
            # layout.addWidget(self.imagelabel)
            # # self.setCentralWidget(self.imagelabel)

            #
            # widget.setGeometry(40,40,256,256)
            # widget.move(10, 10)

            # widget.setLayout(layout)

            self.setMouseTracking(True)
            import pydicom as dicom
            ds = dicom.read_file("G:\\SNAP_Signal_Analysis\\snap_simulation\\SNAP_TOF_Data\\Chang Cheng\\TOF\\IM_0180")
            image = np.array(ds.pixel_array)
            # displagImg(image)
            image = image*ds.RescaleSlope + ds.RescaleIntercept
            self.imagelabel.setImage(image)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()