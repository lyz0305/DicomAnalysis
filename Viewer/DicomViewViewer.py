
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Controller.Log as Log
from Viewer.DicomBasicPanZoomViewer import *
from Viewer.AuxiliaryClass import CharacterDisplayLabel
from Controller import ParaSetting

class ThumbnailViewer(QLabel):

    def __init__(self):
        Log.LogTrace('ThumbnailViewer, Init')
        super(ThumbnailViewer,self).__init__()
        self.seriesName = None
        self.setFixedHeight(ParaSetting.ThumbnailViewHeight)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.info_label = CharacterDisplayLabel()
        # self.info_label.setBackgroundColor(255,255,255)
        self.info_label.setFixedHeight(ParaSetting.ThumbnailSeryNameHeight)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.thumbnail_image = DicomBasicPanZoomViewer()
        self.thumbnail_image.SetPanAble(False)
        self.thumbnail_image.SetZoomAble(False)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.thumbnail_image)

    def setSeriesName(self, str):
        Log.LogTrace('ThumbnailViewer, SetSeriesInfo')
        self.info_label.setText(str)
        self.seriesName = str

    def getSeriesName(self):
        Log.LogTrace('ThumbnailViewer, getSeriesName')
        return self.seriesName

    def setImage(self, image):
        Log.LogTrace('ThumbnailViewer, SetImage')
        self.thumbnail_image.setImage(image)
