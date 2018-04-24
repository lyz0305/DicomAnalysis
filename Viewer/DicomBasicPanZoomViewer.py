
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import numpy as np
from scipy.misc import imresize
import qimage2ndarray
from Viewer.DicomBasicContrastViewer import *
import Controller.Log as Log
import Viewer.EventDecision as Event
import Controller.ParaSetting as Setting

def displagImg(image):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(image,cmap=plt.cm.gray)
    plt.show()


class DicomBasicPanZoomViewer(QLabel):

    def __init__(self,parent=None):
        super(DicomBasicPanZoomViewer,self).__init__(parent)
        Log.LogTrace('DicomBasicPanZoomViewer, Init')
        self.setStyleSheet("background-color:black")
        self.setMouseTracking(True)
        self.setMinimumSize(1,1)
        self.pan = [0,0]


        self.contrastlabel = DicomBasicContrastViewer()
        self.contrastlabelSize = [self.contrastlabel.width(),self.contrastlabel.height()]
        self.contrastlabel.setParent(self)
        height = self.height()
        width = self.width()
        x = width/2-self.contrastlabelSize[0]/2
        y = height/2-self.contrastlabelSize[1]/2
        self.setGeometry(x,y,self.contrastlabelSize[0],self.contrastlabelSize[1])
        self.pressPoint = [-1, -1]
        self.releasePoint = [-1, -1]
        self.currentPoint = [-1, -1]
        self.oldPoint = [-1, -1]

    def contrastLabelPan(self,x,y):
        Log.LogTrace('DicomBasicPanZoomViewer, contrastLabelPan')
        geo = self.contrastlabel.geometry()
        self.contrastlabel.setGeometry(geo.x()+x,geo.y()+y,geo.width(),geo.height())


    def contraslLabelZoom(self,x,y):
        Log.LogTrace('DicomBasicPanZoomViewer, contraslLabelZoom')
        r = min([x,y])
        geo = self.contrastlabel.geometry()
        height = geo.height() + r*Setting.zoomRatio
        width = geo.width() + r*Setting.zoomRatio


        x = geo.x()+geo.width()/2 - width/2
        y = geo.y()+geo.height()/2 - height/2
        self.contrastlabel.setGeometry(x,y,width,height)

    def setImage(self,image):
        '''

        :param image: the input image, a numpy type
        :return:
        '''
        Log.LogTrace('DicomBasicPanZoomViewer, setImage')
        self.originalImg = image
        self.contrastlabel.setImage(image)
        width,height = image.shape
        self.contrastlabel.resize(width,height)
        x = self.width()/2 - width/2
        y = self.height()/2 - height/2
        self.contrastlabel.setGeometry(x,y,width,height)

        self.resizeEvent([])

    def resizeEvent(self, event):
        Log.LogTrace('DicomBasicPanZoomViewer, resizeEvent')

        self.updateViewer()

    def updateViewer(self):
        Log.LogTrace('DicomBasicPanZoomViewer, updateViewer')

        self.contrastlabel.updateViewer()


    def mousePressEvent(self, QMouseEvent):
        Log.LogTrace('DicomBasicPanZoomViewer, mousePressEvent')
        scenePos = QMouseEvent.pos()
        self.pressPoint = [scenePos.x(), scenePos.y()]


        QMouseEvent.ignore()


    def mouseReleaseEvent(self, QMouseEvent):
        Log.LogTrace('DicomBasicPanZoomViewer, mouseReleaseEvent')
        pos = QMouseEvent.pos()
        self.releasePoint = [pos.x(),pos.y()]
        QMouseEvent.ignore()
        pass

    def mouseDoubleClickEvent(self, QMouseEvent):
        Log.LogTrace('DicomBasicPanZoomViewer, mouseDoubleClickEvent')
        QMouseEvent.ignore()
        pass

    def mouseMoveEvent(self, QMouseEvent):
        Log.LogTrace('DicomBasicPanZoomViewer, mouseMoveEvent')
        pos = QMouseEvent.pos()
        self.currentPoint = [pos.x(),pos.y()]

        if self.pressPoint[0] is not -1 and self.pressPoint[1] is not -1:

            if Event.MouseMoveEvent(QMouseEvent) == Event.Pan:
                self.contrastLabelPan(self.currentPoint[0]-self.oldPoint[0],self.currentPoint[1]-self.oldPoint[1])

            elif Event.MouseMoveEvent(QMouseEvent) == Event.Zoom:
                self.contraslLabelZoom(self.currentPoint[0]-self.oldPoint[0],self.currentPoint[1]-self.oldPoint[1])


        self.oldPoint = [pos.x(), pos.y()]
        QMouseEvent.ignore()

        # print([pos.x(), pos.y()])



if __name__ == '__main__':
    Log.removeLog()
    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setWindowTitle("QDicomLabel Test")
            # self.showMaximized()
            self.resize(500,500)

            self.setAttribute(Qt.WA_Hover,True)
            self.setMouseTracking(True)
            self.imagelabel = DicomBasicPanZoomViewer()


            # self.imagelabel.show()
            width = self.imagelabel.width()
            height = self.imagelabel.height()
            self.imagelabel.setGeometry(0, 0,  height,  width)


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