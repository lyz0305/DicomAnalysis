
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Controller.Log as Log
from Viewer.DicomBasicPanZoomViewer import *
from Viewer.AuxiliaryClass import CharacterDisplayLabel

class ThumbnailViewer(QLabel):

    def __init__(self):
        Log.LogTrace('ThumbnailViewer, Init')
        super(ThumbnailViewer,self).__init__()
        self.series = None
        self.setFixedHeight(200)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.info_label = CharacterDisplayLabel()
        self.info_label.setBackgroundColor(255,255,255)
        self.info_label.setFixedHeight(30)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.thumbnail_image = DicomBasicPanZoomViewer()
        self.thumbnail_image.SetPanAble(False)
        self.thumbnail_image.SetZoomAble(False)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.thumbnail_image)

    def setSeriesInfo(self, str):
        Log.LogTrace('ThumbnailViewer, SetSeriesInfo')
        self.info_label.setText(str)
        self.series = str

    def setImage(self, image):
        Log.LogTrace('ThumbnailViewer, SetImage')
        self.thumbnail_image.setImage(image)
