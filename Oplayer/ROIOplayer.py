
from Oplayer.BasicOplayer import BasicOplayer
from Controller.Log import LogClassFuncInfos
from Controller import Status

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import ParaSetting
from Model.DicomViewerModel import ROIModel

class FreeHandROIOplayer(BasicOplayer):

    @LogClassFuncInfos
    def __init__(self,panel):
        super(FreeHandROIOplayer, self).__init__(panel)
        self.__roi = QPolygonF()
        self.__erase = QPolygonF()
        self.__displayROI = QPolygonF()

        self.__pressPoint = [-1, -1]
        self.__releasePoint = [-1, -1]
        self.__currentPoint = [-1, -1]
        self.__lastPoint = [-1, -1]

        self.__roiModel = ROIModel()

    @LogClassFuncInfos
    def setModel(self, model):
        if model.Name is self.__roiModel.Name:
            self.__roiModel = model
            self.__roiModel.AddObserves(self)

    @LogClassFuncInfos
    def update(self, model):
        if model.Name is self.__roiModel.Name:
            self.roiModelChange()

    @LogClassFuncInfos
    def roiModelChange(self):
        roi = self.__roiModel.getROI()
        ROI = QPolygonF()
        for point in roi:
            p = QPointF(point[0], point[1])
            ROI.append(p)
        self.__roi = ROI
        self.updataDisplay()

    @LogClassFuncInfos
    def toROIModel(self):

        roi = []
        for i in range(self.__roi.count()):
            point = self.__roi.at(i)
            p = [point.x(), point.y()]
            roi.append(p)

        self.__roiModel.setROI(roi)

    @LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        x = pos.x()
        y = pos.y()
        self.__currentPoint = [pos.x(), pos.y()]
        if Status.getBTNStatus() is Status.BTNFreeHandROIDraw and self.__pressPoint[0] is not -1 and self.__pressPoint[1] is not -1:
            p = QPointF(x, y)
            self.__displayROI.append(p)

        if Status.getBTNStatus() is Status.BTNFreeHandROIErase and self.__pressPoint[0] is not -1 and self.__pressPoint[1] is not -1:
            p = QPointF(x, y)
            self.__erase.append(p)

        self.__lastPointPoint = [pos.x(), pos.y()]
        self.updateView()

    @LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        scenePos = QMouseEvent.pos()
        self.__pressPoint = [scenePos.x(), scenePos.y()]
        self.__lastPointPoint = [scenePos.x(), scenePos.y()]
        if Status.getBTNStatus() is Status.BTNFreeHandROIDraw:
            self.__displayROI = QPolygonF()

        if Status.getBTNStatus() is Status.BTNFreeHandROIErase:
            self.__erase = QPolygonF()

    @LogClassFuncInfos
    def displayROIToImageROI(self):
        imageROI = QPolygonF()
        for i in range(self.__displayROI.count()):
            point = self.__displayROI.at(i)
            X, Y = self.LabelToImagePosition(point.x(), point.y())
            imageROI.append(QPointF(X, Y))

        self.__roi = imageROI
        self.toROIModel()

    @LogClassFuncInfos
    def updataDisplay(self):

        if self.__roi.count() is 0:
            self.__displayROI = QPolygonF()
            return

        x = []
        y = []
        for i in range(self.__roi.count()):
            point = self.__roi.at(i)
            x.append(point.x())
            y.append(point.y())
        X, Y = self.ImageToLabelPosition(x, y)
        displayROI = QPolygonF()
        for i in range(self.__roi.count()):
            p = QPointF(X[i], Y[i])
            displayROI.append(p)

        self.__displayROI = displayROI

    @LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.__releasePoint = [pos.x(), pos.y()]
        self.__pressPoint = [-1, -1]

        if self.__erase.count() is not 0:
            # cut the area of erase from roi
            # firstly, we find the intersected polygon
            intersectedPolygon = self.__displayROI.intersected(self.__erase)
            # then, we used the roi subtracted the intersected polygon
            newROI = self.__displayROI.subtracted(intersectedPolygon)
            self.__displayROI = newROI
            self.__erase = QPolygonF()

        self.displayROIToImageROI()

    @LogClassFuncInfos
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self.getPanel())

        # draw ROI
        painter.setPen(QColor(ParaSetting.ROIDrawColorR,
                              ParaSetting.ROIDrawColorG,
                              ParaSetting.ROIDrawColorB))

        # labelROI = QPolygonF()
        # for i in range(self.__roi.count()):
        #     point = self.__roi.at(i)
        #     X, Y = self.ImageToLabelPosition(point.x(), point.y())
        #     p = QPointF(X, Y)
        #     labelROI.append(p)
        painter.drawPolygon(self.__displayROI)

        # draw erase
        painter.setPen(QColor(ParaSetting.ROIEraseColorR,
                              ParaSetting.ROIEraseColorG,
                              ParaSetting.ROIEraseColorB))

        # labelROI = QPolygonF()
        # for i in range(self.__erase.count()):
        #     point = self.__erase.at(i)
        #     X, Y = self.ImageToLabelPosition(point.x(), point.y())
        #     p = QPointF(X, Y)
        #     labelROI.append(p)
        painter.drawPolygon(self.__erase)
