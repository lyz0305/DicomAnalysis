
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Controller.Log as Log
from Viewer.DicomBasicPanZoomViewer import *


class ThumbnailViewer(QLabel):

    def __init__(self):
        Log.LogTrace('ThumbnailViewer, Init')
        super(ThumbnailViewer,self).__init__()
        self.series = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.info_label = QLabel()
        self.thumbnail_image = DicomBasicPanZoomViewer()
        self.thumbnail_image.SetPanAble(False)
        self.thumbnail_image.SetZoomAble(False)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.thumbnail_image)

    def SetSeriesInfo(self, str):
        Log.LogTrace('ThumbnailViewer, SetSeriesInfo')
        self.info_label.setText(str)
        self.series = str

    def SetImage(self, image):
        Log.LogTrace('ThumbnailViewer, SetImage')
        self.thumbnail_image.setImage(image)
