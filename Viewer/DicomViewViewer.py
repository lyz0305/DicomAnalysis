
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
        self.selected = False
        self.setFixedHeight(ParaSetting.ThumbnailViewHeight)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.name_label = CharacterDisplayLabel()
        # self.info_label.setBackgroundColor(255,255,255)
        self.name_label.setFixedHeight(ParaSetting.ThumbnailSeryNameHeight)
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.thumbnail_image = DicomBasicPanZoomViewer()
        self.thumbnail_image.SetPanAble(False)
        self.thumbnail_image.SetZoomAble(False)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.thumbnail_image)

    def setSeriesName(self, str):
        Log.LogTrace('ThumbnailViewer, SetSeriesInfo')
        self.name_label.setText(str)
        self.seriesName = str

    def getSeriesName(self):
        Log.LogTrace('ThumbnailViewer, getSeriesName')
        return self.seriesName

    def setImage(self, image):
        Log.LogTrace('ThumbnailViewer, SetImage')
        self.thumbnail_image.setImage(image)

    def setCharacterBackground(self, r, g, b, a):
        Log.LogTrace('ThumbnailViewer, setCharacterBackground')
        self.name_label.setBackgroundColor(r,g,b,a)

    def setSelectState(self, state):
        Log.LogTrace('ThumbnailViewer, setSelectState')
        self.selected = state
        if self.selected is True:
            self.setCharacterBackground(ParaSetting.ThumbnailSelectedColorR,
                                        ParaSetting.ThumbnailSelectedColorG,
                                        ParaSetting.ThumbnailSelectedColorB,
                                        255)
        elif self.selected is False:
            self.setCharacterBackground(ParaSetting.ThumbnailSelectedColorR,
                                        ParaSetting.ThumbnailSelectedColorG,
                                        ParaSetting.ThumbnailSelectedColorB,
                                        0)

    def getSelectState(self):
        Log.LogTrace('ThumbnailViewer, getSelectState')
        return self.selected