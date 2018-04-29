
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from Controller import Log
from Viewer.DicomBasicPanZoomViewer import *
from Viewer.AuxiliaryClass import CharacterDisplayLabel
from Controller import ParaSetting

class ThumbnailViewer(QLabel):

    @Log.LogClassFuncInfos
    def __init__(self):
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
        self.thumbnail_image.setPanAble(False)
        self.thumbnail_image.setZoomAble(False)
        self.thumbnail_image.setContrastAble(False)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.thumbnail_image)

    @Log.LogClassFuncInfos
    def setSeriesName(self, str):
        self.name_label.setText(str)
        self.seriesName = str

    @Log.LogClassFuncInfos
    def getSeriesName(self):
        return self.seriesName

    @Log.LogClassFuncInfos
    def setImage(self, image):
        self.thumbnail_image.setImage(image)

    @Log.LogClassFuncInfos
    def setCharacterBackground(self, r, g, b, a):
        self.name_label.setBackgroundColor(r,g,b,a)

    @Log.LogClassFuncInfos
    def setSelectState(self, state):
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

    @Log.LogClassFuncInfos
    def getSelectState(self):
        return self.selected