
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy as np
import cv2
import qimage2ndarray
from Controller import Log
import Viewer.EventDecision as Event
import Controller.ParaSetting as Setting
from Model.DicomViewerModel import DisplayInfoModel
from Controller import Status

class DicomBasicImageViewer(QLabel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomBasicImageViewer, self).__init__()
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)

        self.__originalImg = None
        self.__zoomImg = None
        self.__displayImg = None

        self.setMinimumSize(1, 1)
        self.__pressPoint = [-1, -1]
        self.__releasePoint = [-1, -1]
        self.__currentPoint = [-1, -1]
        self.__lastPoint = [-1, -1]

        self.__contrast = dict()
        self.__contrast['center'] = -9999
        self.__contrast['width'] = -9999

        self.__imgGeo = dict()
        self.__imgGeo['centerX'] = 0
        self.__imgGeo['centerY'] = 0
        self.__imgGeo['width'] = 0
        self.__imgGeo['height'] = 0

        self.__contrastAble = True
        self.__panAble = True
        self.__zoomAble = True

    @Log.LogClassFuncInfos
    def getOriImgSize(self):
        if self.__originalImg is None:
            return -1, -1
        width, height = self.__originalImg.shape
        return width, height

    @Log.LogClassFuncInfos
    def getCurImgSize(self):
        return self.__imgGeo['width'], self.__imgGeo['height']

    @Log.LogClassFuncInfos
    def getImgPos(self):
        return self.__imgGeo['centerX'], self.__imgGeo['centerY']

    @Log.LogClassFuncInfos
    def setImage(self, image):
        self.__originalImg = image
        self.updateImgSize()

    @Log.LogClassFuncInfos
    def resetParaByImage(self):

        if self.__originalImg is None:
            return

        self.__imgGeo['width'] = self.__originalImg.shape[0]
        self.__imgGeo['height'] = self.__originalImg.shape[1]
        height = self.height()
        width = self.width()
        self.__imgGeo['centerX'] = width/2
        self.__imgGeo['centerY'] = height/2
        self.updateImgSize()

        MIN = self.__zoomImg.min()
        MAX = self.__zoomImg.max()
        center = (MIN + MAX) / 2
        width = (MAX - MIN)
        self.__contrast['center'] = center
        self.__contrast['width'] = width
        self.updateDisplayImage()

    @Log.LogClassFuncInfos
    def resetParaByPanel(self):

        height = self.height()
        width = self.width()

        self.__imgGeo['width'] = width
        self.__imgGeo['height'] = height

        self.__imgGeo['centerX'] = width / 2
        self.__imgGeo['centerY'] = height / 2
        self.updateImgSize()

        if self.__zoomImg is None:
            return

        MIN = self.__zoomImg.min()
        MAX = self.__zoomImg.max()
        center = (MIN + MAX) / 2
        width = (MAX - MIN)
        self.__contrast['center'] = center
        self.__contrast['width'] = width
        self.updateDisplayImage()

    @Log.LogClassFuncInfos
    def updateImgSize(self):
        if self.__originalImg is None:
            return
        size = [self.__imgGeo['width'], self.__imgGeo['height']]
        s = min(size)
        if s < 1:
            return
        # zoomImg = imresize(self.__originalImg, [s, s], 'lanczos', mode='I')
        zoomImg = cv2.resize(self.__originalImg,(s,s),interpolation=cv2.INTER_LANCZOS4)
        self.__zoomImg = zoomImg
        self.updateDisplayImage()

    @Log.LogClassFuncInfos
    def updateDisplayImage(self):
        if self.__zoomImg is None:
            return
        MIN = (2 * self.__contrast['center'] - self.__contrast['width']) / 2.0 + 0.5
        MAX = (2 * self.__contrast['center'] + self.__contrast['width']) / 2.0 + 0.5
        dFactor = 255.0 / (MAX - MIN)
        disImg = (self.__zoomImg - MIN) * dFactor
        disImg[disImg < 0] = 0
        disImg[disImg > 255] = 255
        self.__displayImg = disImg
        self.update()

    @Log.LogClassFuncInfos
    def paintEvent(self, QPaintEvent):
        super(DicomBasicImageViewer, self).paintEvent(QPaintEvent)

        if self.__displayImg is not None:
            disImg = self.__displayImg
            QImg = qimage2ndarray.gray2qimage(disImg)
            x = self.__imgGeo['centerX'] - self.__imgGeo['width']/2
            y = self.__imgGeo['centerY'] - self.__imgGeo['height']/2
            pos = QPoint(x,y)
            source = QRect(0,0,self.__imgGeo['width'], self.__imgGeo['height'])

            painter = QPainter(self)
            painter.drawPixmap(pos, QPixmap.fromImage(QImg), source)

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        super(DicomBasicImageViewer, self).resizeEvent(event)
        self.resetParaByImage()

    @Log.LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        super(DicomBasicImageViewer, self).mousePressEvent(QMouseEvent)
        scenePos = QMouseEvent.pos()
        self.__pressPoint = [scenePos.x(), scenePos.y()]
        self.__lastPointPoint = [scenePos.x(), scenePos.y()]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        super(DicomBasicImageViewer, self).mouseReleaseEvent(QMouseEvent)
        pos = QMouseEvent.pos()
        self.__releasePoint = [pos.x(), pos.y()]
        self.__pressPoint = [-1, -1]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        super(DicomBasicImageViewer, self).mouseMoveEvent(QMouseEvent)
        pos = QMouseEvent.pos()
        self.__currentPoint = [pos.x(), pos.y()]
        if self.__pressPoint[0] is not -1 and self.__pressPoint[1] is not -1:
            dx = self.__currentPoint[0] - self.__lastPointPoint[0]
            dy = self.__currentPoint[1] - self.__lastPointPoint[1]
            if self.__contrastAble and Event.MouseMoveEvent(QMouseEvent) == Event.Contrast:
                self.setContrast(dx=dx, dy=dy)
            if self.__panAble and Event.MouseMoveEvent(QMouseEvent) == Event.Pan:
                self.setPan(dx=dx, dy=dy)
            if self.__zoomAble and Event.MouseMoveEvent(QMouseEvent) == Event.Zoom:
                self.setZoom(dx=dx, dy=dy)


        self.__lastPointPoint = [pos.x(), pos.y()]
        QMouseEvent.ignore()

    @Log.LogClassFuncInfos
    def setContrast(self,dx, dy):

        center = self.__contrast['center'] + dx * Setting.contrastRatio
        width = self.__contrast['width'] + dy * Setting.contrastRatio
        self.__contrast['center'] = center
        self.__contrast['width'] = width
        self.updateDisplayImage()

    @Log.LogClassFuncInfos
    def setPan(self, dx, dy):
        self.__imgGeo['centerX'] = self.__imgGeo['centerX'] + dx
        self.__imgGeo['centerY'] = self.__imgGeo['centerY'] + dy
        self.update()

    @Log.LogClassFuncInfos
    def setZoom(self, dx, dy):
        r = min([dx,dy])
        self.__imgGeo['width'] = self.__imgGeo['width'] + r*Setting.zoomRatio
        self.__imgGeo['height'] = self.__imgGeo['height'] + r*Setting.zoomRatio

        if self.__imgGeo['width'] < 1:
            self.__imgGeo['width'] = 1

        if self.__imgGeo['height'] < 1:
            self.__imgGeo['height'] = 1

        self.updateImgSize()
        self.updateDisplayImage()
        self.update()

    @Log.LogClassFuncInfos
    def setPanAble(self, able):
        self.__panAble = able

    @Log.LogClassFuncInfos
    def setZoomAble(self, able):
        self.__zoomAble = able

    @Log.LogClassFuncInfos
    def setContrastAble(self, able):
        self.__contrastAble = able

class DicomBasicDicomImageViewer(DicomBasicImageViewer):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomBasicDicomImageViewer, self).__init__()
        self.__oplayerList = []
        self.__displayModel = DisplayInfoModel()

    @Log.LogClassFuncInfos
    def setModel(self, model):
        if model.Name is self.__displayModel.Name:
            self.__displayModel = model
        self.setModelDown(model)

    @Log.LogClassFuncInfos
    def setOriImgSizeToOplayer(self):
        width, height = self.getOriImgSize()
        for oplayer in self.__oplayerList:
            oplayer.setOriImgSize(width, height)

    @Log.LogClassFuncInfos
    def setCurImgSizeToOplayer(self):
        width, height = self.getCurImgSize()
        for oplayer in self.__oplayerList:
            oplayer.setCurImgSize(width, height)

    @Log.LogClassFuncInfos
    def setImgPosToOplayer(self):
        centerX, centerY = self.getImgPos()
        for oplayer in self.__oplayerList:
            oplayer.setImgPos(centerX, centerY)

    @Log.LogClassFuncInfos
    def setModelDown(self, model):
        for oplayer in self.__oplayerList:
            oplayer.setModel(model)

    @Log.LogClassFuncInfos
    def paintEvent(self, QPaintEvent):
        super(DicomBasicDicomImageViewer, self).paintEvent(QPaintEvent)
        for oplayer in self.__oplayerList:
            oplayer.paintEvent(QPaintEvent)

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        super(DicomBasicDicomImageViewer, self).resizeEvent(event)
        self.setCurImgSizeToOplayer()
        self.setImgPosToOplayer()
        for oplayer in self.__oplayerList:
            oplayer.resizeEvent(event)

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        super(DicomBasicDicomImageViewer, self).mouseMoveEvent(QMouseEvent)
        self.setCurImgSizeToOplayer()
        self.setImgPosToOplayer()

        for oplayer in self.__oplayerList:
            oplayer.mouseMoveEvent(QMouseEvent)

    @Log.LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        super(DicomBasicDicomImageViewer, self).mousePressEvent(QMouseEvent)
        for oplayer in self.__oplayerList:
            oplayer.mousePressEvent(QMouseEvent)


    @Log.LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        super(DicomBasicDicomImageViewer, self).mouseReleaseEvent(QMouseEvent)
        for oplayer in self.__oplayerList:
            oplayer.mouseReleaseEvent(QMouseEvent)


    @Log.LogClassFuncInfos
    def wheelEvent(self, QEvent):
        super(DicomBasicDicomImageViewer, self).wheelEvent(QEvent)
        for oplayer in self.__oplayerList:
            oplayer.wheelEvent(QEvent)
        delta = QEvent.angleDelta()
        angle = delta.y()
        slice = -angle // 120
        self.__displayModel.instanceChange(slice)

    @Log.LogClassFuncInfos
    def addOplayer(self, oplayer):
        self.__oplayerList.append(oplayer)
        self.setOriImgSizeToOplayer()

if __name__ == '__main__':

    Log.removeLog()

    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setWindowTitle("QDicomLabel Test")
            self.showMaximized()
            # self.resize(500,500)
            # self.setGeometry(400,100,500,200)

            self.setAttribute(Qt.WA_Hover,True)
            self.setMouseTracking(True)
            self.imagelabel = DicomBasicDicomImageViewer()

            self.setCentralWidget(self.imagelabel)

            self.setMouseTracking(True)
            import pydicom as dicom
            ds = dicom.read_file("G:\\SNAP_Signal_Analysis\\snap_simulation\\SNAP_TOF_Data\\Chang Cheng\\TOF\\IM_0180")
            image = np.array(ds.pixel_array)
            # # displagImg(image)
            image = image*ds.RescaleSlope + ds.RescaleIntercept
            self.imagelabel.setImage(image)
            # self.imagelabel.resetParaByImage()

            # self.imagelabel.resetContrast()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()