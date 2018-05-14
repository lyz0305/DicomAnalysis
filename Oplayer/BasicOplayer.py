
from Controller import Log
import numpy as np

class BasicOplayer():

    def __init__(self, panel):
        self.Name = self.__class__.__name__
        self.__panel = panel

        self.__oriWidth = -1
        self.__oriHeight = -1

        self.__curWidth = -1
        self.__curHeight = -1

        self.__centerX = -1
        self.__centerY = -1

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        pass

    @Log.LogClassFuncInfos
    def setOriImgSize(self, width, height):
        self.__oriWidth = width
        self.__oriHeight = height

    @Log.LogClassFuncInfos
    def updataDisplay(self):
        pass

    @Log.LogClassFuncInfos
    def getOriImgSize(self):
        return self.__oriWidth, self.__oriHeight

    @Log.LogClassFuncInfos
    def getCurImgSize(self):
        return self.__curWidth, self.__curHeight

    @Log.LogClassFuncInfos
    def getImgPos(self):
        return self.__centerX, self.__centerY

    @Log.LogClassFuncInfos
    def setCurImgSize(self, width, height):

        if self.__curHeight is not height or self.__curWidth is not width:

            self.__curWidth = width
            self.__curHeight = height
            self.updataDisplay()

    @Log.LogClassFuncInfos
    def setImgPos(self, centerX, centerY):

        if self.__centerX is not centerX or self.__centerY is not centerY:

            self.__centerX = centerX
            self.__centerY = centerY
            self.updataDisplay()

    @Log.LogClassFuncInfos
    def setModel(self, model):
        pass

    @Log.LogClassFuncInfos
    def mousePressEvent(self, QMouseEvent):
        pass


    @Log.LogClassFuncInfos
    def mouseReleaseEvent(self, QMouseEvent):
        pass


    @Log.LogClassFuncInfos
    def wheelEvent(self, QEvent):
        pass

    @Log.LogClassFuncInfos
    def paintEvent(self, QPaintEvent):
        pass

    @Log.LogClassFuncInfos
    def getPanel(self):
        return self.__panel

    @Log.LogClassFuncInfos
    def updateView(self):
        self.__panel.update()

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        self.updataDisplay()
        self.updateView()

    @Log.LogClassFuncInfos
    def LabelToImagePosition(self, x, y):
        curWidth, curHeight = self.getCurImgSize()
        centerX, centerY = self.getImgPos()
        # first, we need to calculate the position in the zoomed image
        rX = x - centerX + 1 / 2 * curWidth
        rY = y - centerY + 1 / 2 * curHeight
        # then, the zoom factor should be considered
        oriWidth, oriHeight = self.getOriImgSize()
        X = rX / curWidth * oriWidth
        Y = rY / curHeight * oriHeight  # finally, we get the position in the original image
        return X, Y

    @Log.LogClassFuncInfos
    def ImageToLabelPosition(self, x, y):
        # the inversion operation of LabelToImagePosition
        x = np.array(x)
        y = np.array(y)

        curWidth, curHeight = self.getCurImgSize()
        oriWidth, oriHeight = self.getOriImgSize()

        rX = x/oriWidth*curWidth
        rY = y/oriHeight*curHeight

        centerX, centerY = self.getImgPos()
        X = rX - 1/2*curWidth + centerX
        Y = rY - 1/2*curHeight + centerY
        return X, Y