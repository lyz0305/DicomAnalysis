
from Controller.Observe import *
from Controller.Log import *
from Controller.DicomViewerBaseController import *
from Model.DicomViewerModel import *
import SimpleITK as sitk
from Controller.TagName import Tags
from Viewer.DicomViewViewer import ThumbnailViewer
from Viewer.AuxiliaryClass import CharacterDisplayLabel, ThumbnailListWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import ParaSetting


class DicomToolViewController(DicomViewerBasePanelController, Observe):

    def __init__(self):
        LogTrace('DicomToolViewController, Init')
        self.Name = 'DicomToolViewController'
        super(DicomToolViewController, self).__init__()
        self.layout = QHBoxLayout()

    def InitGUI(self):
        LogTrace('DicomToolViewController, InitGUI')

    def InitModel(self):
        LogTrace('DicomToolViewController, InitModel')

    def Update(self,model):
        LogTrace('DicomToolViewController, Update')

    def SetModel(self, model):
        LogTrace('DicomToolViewController, SetModel,'+model.Name)

    def SetLayout(self, layout):
        LogTrace('DicomToolViewController, SetLayout')
        self.layout = layout

class DicomToolMainPanelController(DicomViewerBasePanelController, Observe):

    def __init__(self):
        LogTrace('DicomToolMainPanelController, Init')
        self.Name = 'DicomToolMainPanelController'
        super(DicomToolMainPanelController,self).__init__()
        self.layout = QHBoxLayout()
        self.DisplayModelsModel = None

    def InitGUI(self):
        LogTrace('DicomToolMainPanelController, InitGUI')

    def InitModel(self):
        LogTrace('DicomToolMainPanelController, InitModel')
        self.DisplayModelsModel = DisplayModelsModel()


    def Update(self,model):
        LogTrace('DicomToolMainPanelController, Update')

    def SetModel(self, model):
        LogTrace('DicomToolMainPanelController, SetModel,'+model.Name)
        if model.Name == self.DisplayModelsModel.Name:
            self.DisplayModelsModel.Name = model
            self.DisplayModelsModel.AddObserves(self)


    def SetLayout(self, layout):
        LogTrace('DicomToolMainPanelController, SetLayout')
        self.layout = layout


class DicomToolThumbnailController(DicomViewerBasePanelController,Observe):
    def __init__(self):
        LogTrace('DicomToolThumbnailController, Init')
        super(DicomToolThumbnailController,self).__init__()
        self.Name = 'DicomToolThumbnailController'
        self.listWidgets = []
        self.layout = QHBoxLayout()
        self.SequenceModel = SequenceModel()
        self.SequenceInfoModel = SequenceInfoModel()
        self.DisplayModelsModel = DisplayModelsModel()

    def InitGUI(self):
        LogTrace('DicomToolThumbnailController, InitGUI')

    def InitModel(self):
        LogTrace('DicomToolThumbnailController, InitModel')

    def Update(self,model):
        LogTrace('DicomToolThumbnailController, InitModel')
        if model.Name == self.SequenceInfoModel.Name:
            self.SequenceInfoChange()

    def updatePatient(self):
        LogTrace('DicomToolThumbnailController, updatePatient')
        SequenceInfos = self.SequenceInfoModel.GetSequenceInfo()

        patients = None
        for patientName in SequenceInfos.keys():
            for listWidget in self.listWidgets:
                if patientName is not listWidget.getPatientName:
                    patients = patientName

        if patients is None:
            listWidget = ThumbnailListWidget()
            listWidget.setPatientName(patientName)
            listWidget.setContentsMargins(0, 0, 0, 0)
            # listWidget.verticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            listWidget.horizontalOffset()
            # listWidget.horizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # listWidget.horizontalScrollBar().setDisabled(True)
            listWidget.setFixedWidth(ParaSetting.ThumbnailWidgetWidth)
            listWidget.setStyleSheet("background-color: rgb(150, 150, 150)")
            self.layout.addWidget(listWidget)
            self.listWidgets.append(listWidget)
            dicomName = list(list(SequenceInfos[patientName].values())[0].values())[0]

            reader = sitk.ImageFileReader()
            reader.SetFileName(dicomName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            patient_name = reader.GetMetaData(Tags['PatientName'])
            patient_birth = reader.GetMetaData(Tags['DataOfBirth'])

            patient_info = CharacterDisplayLabel()
            patient_info.setText('%s\t\n%s'%(patient_name,patient_birth))
            patient_info.setCharacterColor(Qt.white)
            patient_info.setBackgroundColor(225,109,9)

            patient_info_widgetItem = QListWidgetItem()

            print(ParaSetting.ThumbnailPatientNameHeight, ParaSetting.ThumbnailWidgetWidth)
            # patient_info_widgetItem.setSizeHint(QSize(150, 40))
            patient_info_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailWidgetWidth,ParaSetting.ThumbnailPatientNameHeight))
            # patient_info_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailPatientNameHeight,ParaSetting.ThumbnailWidgetWidth))
            listWidget.addItem(patient_info_widgetItem)
            listWidget.setItemWidget(patient_info_widgetItem,patient_info)
            #
            # thum = ThumbnailViewer()
            # thum.setSeriesName('random')
            # thum_widgetItem = QListWidgetItem()
            # thum_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailWidgetWidth, ParaSetting.ThumbnailViewHeight))
            # # thum_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailViewHeight, ParaSetting.ThumbnailWidgetWidth))
            # listWidget.addItem(thum_widgetItem)
            # listWidget.setItemWidget(thum_widgetItem, thum)


    def SequenceInfoChange(self):
        LogTrace('DicomToolThumbnailController, SequenceNamesChange')
        SequenceInfos = self.SequenceInfoModel.GetSequenceInfo()
        self.updatePatient()
        for patientName in SequenceInfos.keys():
            for listWidget in self.listWidgets:

                if listWidget.count() == len( SequenceInfos[patientName].keys()) + 1:
                    continue

                if patientName is listWidget.getPatientName():
                    series = SequenceInfos[patientName]
                    n = listWidget.count()
                    for sery in series.keys():
                        Exist = False
                        for i in range(n):
                            widgetItem = listWidget.item(i)
                            widget = listWidget.itemWidget(widgetItem)

                            if isinstance(widget, ThumbnailViewer):
                                if sery is widget.getSeriesName():
                                    Exist = True

                        if Exist is False:
                            thum = ThumbnailViewer()
                            thum.setSeriesName(sery)
                            thum_widgetItem = QListWidgetItem()
                            thum_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailWidgetWidth, ParaSetting.ThumbnailViewHeight))

                            # thum_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailViewHeight, ParaSetting.ThumbnailWidgetWidth))
                            listWidget.addItem(thum_widgetItem)
                            listWidget.setItemWidget(thum_widgetItem, thum)


    def SetModel(self, model):
        LogTrace('DicomToolThumbnailController, SetModel,'+model.Name)
        if model.Name is self.SequenceModel.Name:
            self.SequenceModel = model
            model.AddObserves(self)
        elif model.Name is self.SequenceInfoModel.Name:
            self.SequenceInfoModel = model
            model.AddObserves(self)
        elif model.Name is self.DisplayModelsModel.Name:
            self.DisplayModelsModel = model
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
        self.DisplayModelsModel = DisplayModelsModel()

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
        self.MainPanelController.SetModel(self.DisplayModelsModel)
        self.ThumbnailControlelr.SetModel(self.DisplayModelsModel)

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
            patient_name = reader.GetMetaData(Tags['PatientName'])
            name = series_number + ' ' + series_description
            SequenceInfo = self.SequenceInfoModel.GetSequenceInfo()
            if patient_name not in SequenceInfo.keys():
                SequenceInfo[patient_name] = dict()
            if name not in SequenceInfo[patient_name].keys():
                SequenceInfo[patient_name][name] = dict()
            SequenceInfo[patient_name][name][int(instance_number)] = ImageNames[i]

            self.SequenceInfoModel.SetSequenceInfo(SequenceInfo)

if __name__ == '__main__':

    a = DicomToolPageController()
    b = DicomToolPageController()



