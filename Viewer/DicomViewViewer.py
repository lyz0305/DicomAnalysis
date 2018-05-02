
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from Controller import Log
from Viewer.DicomBasicPanZoomViewer import *
from Viewer.AuxiliaryClass import CharacterDisplayLabel
from Controller import ParaSetting

class ThumbnailViewer(QLabel):
    '''
    display a thumbnial, including the sery name and the image
    '''
    @Log.LogClassFuncInfos
    def __init__(self):
        super(ThumbnailViewer,self).__init__()
        self.__seryName = None
        self.__patientName = None
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
        self.thumbnail_image = ThumbnailImageViewer()
        # self.thumbnail_image = DicomBasicPanZoomViewer()
        self.thumbnail_image.setPanAble(False)
        self.thumbnail_image.setZoomAble(False)
        self.thumbnail_image.setContrastAble(False)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.thumbnail_image)

    @Log.LogClassFuncInfos
    def setSeryName(self, str):
        self.name_label.setText(str)
        self.__seryName = str

    @Log.LogClassFuncInfos
    def getSeryName(self):
        return self.__seryName

    @Log.LogClassFuncInfos
    def setPatientName(self, patientName):
        self.__patientName = patientName

    @Log.LogClassFuncInfos
    def getPatientName(self):
        return self.__patientName

    @Log.LogClassFuncInfos
    def setImage(self, image):
        self.thumbnail_image.setImage(image)
        self.thumbnail_image.resetContrast()

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

class ThumbnailImageViewer(DicomBasicPanZoomViewer):

    @Log.LogClassFuncInfos
    def __init__(self, parent=None):
        super(ThumbnailImageViewer, self).__init__(parent)

    @Log.LogClassFuncInfos
    def resizeEvent(self, event):
        geo = self.geometry()
        self.getContrastLabel().resize(self.width(), self.height())
        # self.__contrastlabel.resize(self.width(), self.height())
        self.updateViewer()