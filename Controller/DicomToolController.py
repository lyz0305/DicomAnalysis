
from Controller.Observe import *
from Controller.Log import *
from Controller.DicomToolBaseController import *
from Model.DicomViewerModel import *
import SimpleITK as sitk
from Controller.TagName import Tags

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DicomToolMainPanelController(DicomToolBasePanelController, Observe):

    def __init__(self):
        LogTrace('DicomToolMainPanelController, Init')
        self.Name = 'DicomToolMainPanelController'
        super(DicomToolMainPanelController,self).__init__()
        self.layout = QHBoxLayout()

    def InitGUI(self):
        LogTrace('DicomToolMainPanelController, InitGUI')

    def InitModel(self):
        LogTrace('DicomToolMainPanelController, InitModel')

    def Update(self,model):
        LogTrace('DicomToolMainPanelController, Update')

    def SetModel(self, model):
        LogTrace('DicomToolMainPanelController, SetModel,'+model.Name)

    def SetLayout(self, layout):
        LogTrace('DicomToolMainPanelController, SetLayout')
        self.layout = layout


class DicomToolThumbnailController(DicomToolBasePanelController,Observe):
    def __init__(self):
        LogTrace('DicomToolThumbnailController, Init')
        super(DicomToolThumbnailController,self).__init__()
        self.Name = 'DicomToolThumbnailController'
        self.listWidget = None
        self.layout = QHBoxLayout()
        self.SequenceModel = SequenceModel()
        self.SequenceInfoModel = SequenceInfoModel()

    def InitGUI(self):
        LogTrace('DicomToolThumbnailController, InitGUI')

    def InitModel(self):
        LogTrace('DicomToolThumbnailController, InitModel')

    def Update(self,model):
        LogTrace('DicomToolThumbnailController, InitModel')
        if model.Name == 'SequenceInfoModel':
            self.SequenceNamesChange()

    def SequenceNamesChange(self):
        LogTrace('DicomToolThumbnailController, SequenceNamesChange')
        SequenceInfos = self.SequenceInfoModel.GetSequenceInfo()
        if self.listWidget is None:
            listWidget = QListWidget()
            listWidget.setFixedWidth(200)
            listWidget.setStyleSheet("background: rgb(150, 150, 150)")

            self.layout.addWidget(listWidget)
            self.listWidget = listWidget


        else:
            pass

    def SetModel(self, model):
        LogTrace('DicomToolThumbnailController, SetModel,'+model.Name)
        if model.Name is 'SequenceModel':
            self.SequenceModel = model
            model.AddObserves(self)
        elif model.Name is 'SequenceInfoModel':
            self.SequenceInfoModel = model
            model.AddObserves(self)


    def SetLayout(self, layout):
        LogTrace('DicomToolThumbnailController, SetLayout')
        self.layout = layout

class DicomToolPageController(Observe):

    def __init__(self):
        LogTrace('DicomToolMainController, Init')
        super(DicomToolPageController,self).__init__()
        self.Name = 'DicomToolPageController'
        self.MainPanelController = DicomToolMainPanelController()
        self.ThumbnailControlelr = DicomToolThumbnailController()
        self.InitModel()

    def InitModel(self):
        LogTrace('DicomToolMainController, InitModel')


        self.ImageNamesModel = ImageNamesModel()
        self.SequenceModel = SequenceModel()
        self.SequenceInfoModel = SequenceInfoModel()

        self.ImageNamesModel.AddObserves(self)
        self.SequenceModel.AddObserves(self)
        # self.SequenceInfoModel.AddObserves(self)

        self.MainPanelController.InitModel()
        self.ThumbnailControlelr.InitModel()
        self.SetModelDown()

    def InitGUI(self):
        LogTrace('DicomToolMainController, InitGUI')
        self.MainPanelController.InitGUI()
        self.ThumbnailControlelr.InitGUI()

    def SetModelDown(self):
        LogTrace('DicomToolMainController, SetModelDown')
        self.MainPanelController.SetModel(self.ImageNamesModel)
        self.ThumbnailControlelr.SetModel(self.ImageNamesModel)
        self.MainPanelController.SetModel(self.SequenceModel)
        self.ThumbnailControlelr.SetModel(self.SequenceModel)
        self.ThumbnailControlelr.SetModel(self.SequenceInfoModel)

    def SetLayout(self, layout):
        LogTrace('DicomToolMainController, SetLayout')
        self.layout = layout
        thumbnailLayout = QHBoxLayout()
        mainPanalLayout = QHBoxLayout()

        self.layout.addLayout(thumbnailLayout)
        self.layout.addLayout(mainPanalLayout)
        self.MainPanelController.SetLayout(mainPanalLayout)
        self.ThumbnailControlelr.SetLayout(thumbnailLayout)


    def SetModel(self, model):
        LogTrace('DicomToolMainController, SetModel,'+model.Name)
        if model.Name == 'ImageNamesModel':
            self.ImageNamesModel = model
            self.ImageNamesModel.AddObserves(self)


        self.SetModelDown()

    def Update(self,model):
        LogTrace('DicomToolMainController, Update,'+model.Name)
        if model.Name == 'ImageNamesModel':
            self.ImageNamesChange()

    def ImageNamesChange(self):
        LogTrace('DicomToolMainController, ImageNamesChange')
        ImageNames = self.ImageNamesModel.GetImageNames()
        N = len(ImageNames)
        reader = sitk.ImageFileReader()
        for i in range(N):
            name = ImageNames[i]
            reader.SetFileName(name)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            series_description = reader.GetMetaData(Tags['SeriesDescription'])
            series_number = reader.GetMetaData(Tags['SeriesNumber'])
            instance_number = reader.GetMetaData(Tags['InstanceNumber'])
            name = series_number + ' ' + series_description
            SequenceInfo = self.SequenceInfoModel.GetSequenceInfo()
            if name not in SequenceInfo.keys():
                SequenceInfo[name] = dict()
            SequenceInfo[name][str(instance_number)] = ImageNames[i]

            self.SequenceInfoModel.SetSequenceInfo(SequenceInfo)

if __name__ == '__main__':

    a = DicomToolPageController()
    b = DicomToolPageController()



