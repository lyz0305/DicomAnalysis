
from Controller import Log

class BasicOplayer():

    def __init__(self, painter):
        self.__painter = painter

    @Log.LogClassFuncInfos
    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
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
    def QPaintEvent(self, QPaintEvent):
        pass

    @Log.LogClassFuncInfos
    def getPainter(self):
        return self.__painter