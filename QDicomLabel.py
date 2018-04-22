
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
from scipy.misc import imresize
import qimage2ndarray

def displagImg(image):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(image,cmap=plt.cm.gray)
    plt.show()

class QDicomLabel_contrast(QLabel):
    def __init__(self,parent=None):
        super(QDicomLabel_contrast,self).__init__(parent)
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)
        self.setMinimumSize(1,1)
        self.contrast = dict()
        self.pressPoint = [-1,-1]
        self.releasePoint = [-1,-1]
        self.currentPoint = [-1,-1]
        self.oldPoint = [-1,-1]

    def setImage(self,image):
        self.originalImg = image
        MIN = image.min()
        MAX = image.max()
        center = (MIN+MAX)/2
        width = (MAX-MIN)
        self.contrast['center'] = center
        self.contrast['width'] = width
        self.updateViewer()

    def updateViewer(self):
        MIN = (2*self.contrast['center'] - self.contrast['width'])/2.0 + 0.5
        MAX = (2*self.contrast['center'] + self.contrast['width'])/2.0 + 0.5
        dFactor = 255.0/(MAX-MIN)
        disImg = (self.originalImg - MIN)*dFactor
        disImg[disImg<0] = 0
        disImg[disImg>255] = 255
        QImg = qimage2ndarray.gray2qimage(disImg)
        self.setPixmap(QPixmap.fromImage(QImg))

    def mousePressEvent(self, QMouseEvent):
        scenePos = QMouseEvent.pos()
        self.pressPoint = [scenePos.x(), scenePos.y()]
        self.oldPoint = [scenePos.x(), scenePos.y()]
        pass

    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.releasePoint = [pos.x(), pos.y()]
        self.pressPoint = [-1,-1]
        pass

    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.currentPoint = [pos.x(), pos.y()]
        if self.pressPoint[0] is not -1 and self.pressPoint[1] is not -1:
            dx = self.currentPoint[0] - self.oldPoint[0]
            dy = self.currentPoint[1] - self.oldPoint[1]
            ratio = 5
            self.contrast['center'] = self.contrast['center'] + dx*ratio
            self.contrast['width'] = self.contrast['width'] + dy*ratio
            self.updateViewer()
            # print(self.contrast['center'],self.contrast['width'])

        pass

        self.oldPoint = [pos.x(), pos.y()]

class QDicomLabel_zoom_pan(QLabel):

    def __init__(self,parent=None):
        super(QDicomLabel_zoom_pan,self).__init__(parent)
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)
        # self.setScaledContents(True)
        self.setMinimumSize(1,1)
        self.zoomRatio = 1

    def setImage(self,image):
        '''

        :param image: the input image, a numpy type
        :return:
        '''
        self.originalImg = image
        self.resizeEvent([])

    def resizeEvent(self, event):

        label_width = self.width()
        label_heigth = self.height()
        w, h = self.originalImg.shape
        r1 = label_width / w
        r2 = label_heigth / h
        self.zoomRatio = min([r1, r2])

        self.updateViewer()

    def updateViewer(self):

        size = [self.originalImg.shape[0]*self.zoomRatio, self.originalImg.shape[1]*self.zoomRatio]
        zoomImg = imresize(self.originalImg,[int(size[0]),int(size[1])],'lanczos')
        panImg = np.zeros(zoomImg.shape)
        # panImg[]
        self.QImg = qimage2ndarray.gray2qimage(zoomImg)
        self.setPixmap(QPixmap.fromImage(self.QImg))
        pass

    def mousePressEvent(self, QMouseEvent):
        scenePos = QMouseEvent.pos()
        self.prePoint = [scenePos.x(), scenePos.y()]
        if QMouseEvent.button() == Qt.LeftButton:

            pass
        elif QMouseEvent.button() == Qt.RightButton:

            pass

        elif QMouseEvent.button() == Qt.MiddleButton:

            pass


    def mouseReleaseEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.releasePoint = [pos.x(),pos.y()]
        pass

    def mouseDoubleClickEvent(self, QMouseEvent):

        pass

    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.currentPoint = [pos.x(),pos.y()]
        # print(self.currentPoint)
        pass


if __name__ == '__main__':

    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setWindowTitle("QDicomLabel Test")
            self.imagelabel = QDicomLabel_contrast()
            width = self.imagelabel.width()
            height = self.imagelabel.height()
            self.setCentralWidget(self.imagelabel)
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