
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
from scipy.misc import imresize
import qimage2ndarray
from Viewer.DicomBasicContrastViewer import *
import Controller.Log as Log
from Controller import Log
import Viewer.EventDecision as Event
import Controller.ParaSetting as Setting
from Model.DicomViewerModel import DisplayInfoModel


class DicomBasicPanZoomViewer(QLabel):

    @Log.LogClassFuncInfos
    def __init__(self,parent=None):
        super(DicomBasicPanZoomViewer,self).__init__(parent)
        self.__panAble = True
        self.__zoomAble = True
        self.__contrastAble = True
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)
        self.setMinimumSize(1,1)
        self.__pan = [0,0]


        self.__contrastlabel = DicomBasicContrastViewer()
        self.contrastlabelSize = [self.__contrastlabel.width(),self.__contrastlabel.height()]
        self.__contrastlabel.setParent(self)
        height = self.height()
        width = self.width()
        x = width/2-self.contrastlabelSize[0]/2
        y = height/2-self.contrastlabelSize[1]/2
        self.__contrastlabel.setGeometry(x,y,self.contrastlabelSize[0],self.contrastlabelSize[1])
        self.pressPoint = [-1, -1]
        self.releasePoint = [-1, -1]
        self.currentPoint = [-1, -1]
        self.oldPoint = [-1, -1]

        self.__displayModel = DisplayInfoModel()
    @Log.LogClassFuncInfos
    def contrastLabelPan(self,x,y):
        geo = self.__contrastlabel.geometry()
        self.__contrastlabel.setGeometry(geo.x()+x,geo.y()+y,geo.width(),geo.height())

    @Log.LogClassFuncInfos
    def getContrast(self):
        return self.__contrastlabel.getContrast()

    @Log.LogClassFuncInfos
    def getPan(self):
        geo = self.__contrastlabel.geometry()
        return geo.x(), geo.y()

    @Log.LogClassFuncInfos
    def setContrast(self, center, width):
        self.__contrastlabel.setContrast(center, width)

    @Log.LogClassFuncInfos
    def contraslLabelZoom(self,x,y):
        r = min([x,y])
        geo = self.__contrastlabel.geometry()
        height = geo.height() + r*Setting.zoomRatio
        width = geo.width() + r*Setting.zoomRatio

        self.setSize(width, height)
        # x = geo.x()+geo.width()/2 - width/2
        # y = geo.y()+geo.height()/2 - height/2
        # self.__contrastlabel.setGeometry(x,y,width,height)

    # @Log.LogClassFuncInfos
    def setSize(self, width, height):
        '''
        to set the size of contrast label
        :param width:
        :param height:
        :return:
        '''
        geo = self.__contrastlabel.geometry()
        x = geo.x() + geo.width() / 2 - width / 2
        y = geo.y() + geo.height() / 2 - height / 2
        self.__contrastlabel.setGeometry(x, y, width, height)

    @Log.LogClassFuncInfos
    def setModel(self, model):

        if model.Name is self.__displayModel.Name:
            self.__displayModel = model

    @Log.LogClassFuncInfos
    def setImage(self,image):
        '''

        :param image: the input image, a numpy type
        :return:
        '''
        self.__originalImg = image
        self.__contrastlabel.setImage(image)

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        geo = self.geometry()
        if self.__originalImg is not None:
            imgWidth, imgHeight = self.__originalImg.shape
            geo = self.geometry()
            panelWidth = geo.width()
            panelHeight = geo.height()
            x = panelWidth / 2 - imgWidth / 2
            y = panelHeight / 2 - imgHeight / 2
            self.__contrastlabel.setGeometry(x, y, imgWidth, imgHeight)
        else:
            self.__contrastlabel.resize(self.width(), self.height())
        self.updateViewer()

    @Log.LogClassFuncInfos
    def updateViewer(self):
        self.__contrastlabel.updateViewer()

    @Log.LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        scenePos = QMouseEvent.pos()
        self.pressPoint = [scenePos.x(), scenePos.y()]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.releasePoint = [pos.x(),pos.y()]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseDoubleClickEvent(self, QMouseEvent):
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def setPanAble(self, able):
        self.__panAble = able

    @Log.LogClassFuncInfos
    def setZoomAble(self, able):
        self.__zoomAble = able

    @Log.LogClassFuncInfos
    def setContrastAble(self, able):
        self.__contrastAble = able
        self.__contrastlabel.SetContrastAble(able)

    @Log.LogClassFuncInfos
    def getContrastLabel(self):
        return self.__contrastlabel

    @Log.LogClassFuncInfos
    def resetContrast(self):
        self.__contrastlabel.resetContrast()

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.currentPoint = [pos.x(),pos.y()]

        if self.pressPoint[0] is not -1 and self.pressPoint[1] is not -1:

            if self.__panAble and Event.MouseMoveEvent(QMouseEvent) == Event.Pan:
                self.contrastLabelPan(self.currentPoint[0]-self.oldPoint[0],self.currentPoint[1]-self.oldPoint[1])

            elif self.__zoomAble and Event.MouseMoveEvent(QMouseEvent) == Event.Zoom:
                self.contraslLabelZoom(self.currentPoint[0]-self.oldPoint[0],self.currentPoint[1]-self.oldPoint[1])


        self.oldPoint = [pos.x(), pos.y()]
        QMouseEvent.ignore()

        # print([pos.x(), pos.y()])

    @Log.LogClassFuncInfos
    def wheelEvent(self, QEvent):
        delta = QEvent.angleDelta()
        angle = delta.y()
        slice = angle//120
        self.__displayModel.instenceChange(slice)

if __name__ == '__main__':

    class TestClass(DicomBasicPanZoomViewer):
        def __init__(self):
            super(DicomBasicPanZoomViewer, self).__init__()

    # a = TestClass()
    Log.removeLog()
    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setWindowTitle("QDicomLabel Test")
            self.showMaximized()
            # self.resize(500,500)

            self.setAttribute(Qt.WA_Hover,True)
            self.setMouseTracking(True)
            self.imagelabel = DicomBasicPanZoomViewer()


            # self.imagelabel.show()
            width = self.imagelabel.width()
            height = self.imagelabel.height()
            # self.imagelabel.setGeometry(0, 0,  height,  width)


            # layout = QHBoxLayout()
            # layout.addWidget(self.imagelabel)
            # # self.setCentralWidget(self.imagelabel)

            #
            # widget.setGeometry(40,40,256,256)
            # widget.move(10, 10)
            self.setCentralWidget(self.imagelabel)
            # widget.setLayout(layout)

            self.setMouseTracking(True)
            import dicom
            ds = dicom.read_file("G:\\SNAP_Signal_Analysis\\snap_simulation\\SNAP_TOF_Data\\Chang Cheng\\TOF\\IM_0180")
            image = np.array(ds.pixel_array)
            # displagImg(image)
            image = image*ds.RescaleSlope + ds.RescaleIntercept
            self.imagelabel.setImage(image)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()