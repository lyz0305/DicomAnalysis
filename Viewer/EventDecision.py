from PyQt5.QtCore import Qt
from Controller import Status

Other = -1
Pan = 0
Zoom = 1
Contrast = 2
BrowsePage = 3

def MouseMoveEvent(QMouseEvent):
    '''
    decide the event when mouse move
    :param QMouseEvent:
    :return:
    '''
    if Status.getBTNStatus() is not Status.BTNNormal:
        return Other
    if QMouseEvent.buttons() == Qt.LeftButton:
        return Pan
    elif QMouseEvent.buttons() == Qt.MidButton:
        return Contrast
    elif QMouseEvent.buttons() == Qt.RightButton:
        return Zoom


