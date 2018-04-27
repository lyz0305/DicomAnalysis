
from Controller.Observe import *
from Controller.Log import *
from Controller.DicomViewerBaseController import *
from Model.DicomViewerModel import *
import SimpleITK as sitk
from Controller.TagName import Tags
from Viewer.DicomViewViewer import ThumbnailViewer
from Viewer.AuxiliaryClass import CharacterDisplayLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DicomToolMainPanelController(DicomViewerBasePanelController, Observe):

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


class DicomToolThumbnailController(DicomViewerBasePanelController,Observe):
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
        if model.Name == self.SequenceInfoModel.Name:
            self.SequenceInfoChange()

    def SequenceInfoChange(self):
        LogTrace('DicomToolThumbnailController, SequenceNamesChange')
        SequenceInfos = self.SequenceInfoModel.GetSequenceInfo()
        if self.listWidget is None:
            listWidget = QListWidget()
            listWidget.setFixedWidth(150)
            # listWidget.setStyleSheet("QListWidget: item { border-bottom: 5px solid black; }")
            listWidget.setStyleSheet("background: rgb(150, 150, 150)")
            # listWidget.setStyleSheet("QListWidget: item { border-bottom: 5px solid black; }; background: rgb(150, 150, 150)")

            self.layout.addWidget(listWidget)
            self.listWidget = listWidget

            name = list(list(SequenceInfos.values())[0].values())[0]
            reader = sitk.ImageFileReader()
            reader.SetFileName(name)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            patient_name = reader.GetMetaData(Tags['PatientName'])
            patient_birth = reader.GetMetaData(Tags['DataOfBirth'])

            patient_info = CharacterDisplayLabel()
            patient_info.setText('%s\t\n%s'%(patient_name,patient_birth))
            patient_info.setCharacterColor(Qt.white)
            patient_info.setBackgroundColor(225,109,9)

            patient_info_widgetItem = QListWidgetItem()
            patient_info_widgetItem.setSizeHint(QSize(40,60))
            self.listWidget.addItem(patient_info_widgetItem)
            self.listWidget.setItemWidget(patient_info_widgetItem,patient_info)

            thum = ThumbnailViewer()
            thum.setSeriesInfo(list(SequenceInfos.keys())[0])
            thum_widgetItem = QListWidgetItem()
            self.listWidget.addItem(thum_widgetItem)
            self.listWidget.setItemWidget(thum_widgetItem, thum)

        else:
            pass

    def SetModel(self, model):
        LogTrace('DicomToolThumbnailController, SetModel,'+model.Name)
        if model.Name is self.SequenceModel.Name:
            self.SequenceModel = model
            model.AddObserves(self)
        elif model.Name is self.SequenceInfoModel.Name:
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
        self.layout.addStretch()
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
        if model.Name == self.ImageNamesModel.Name:
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



