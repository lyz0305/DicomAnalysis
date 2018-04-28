
from Controller.Observe import *
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
from Controller import Log


class DicomToolViewController(DicomViewerBasePanelController, Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolViewController'
        super(DicomToolViewController, self).__init__()
        self.layout = QHBoxLayout()

    @Log.LogClassFuncInfos
    def InitGUI(self):
        pass

    @Log.LogClassFuncInfos
    def InitModel(self):
        pass

    @Log.LogClassFuncInfos
    def Update(self,model):
        pass

    @Log.LogClassFuncInfos
    def SetModel(self, model):
        pass

    @Log.LogClassFuncInfos
    def SetLayout(self, layout):
        pass
        self.layout = layout

class DicomToolMainPanelController(DicomViewerBasePanelController, Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolMainPanelController'
        super(DicomToolMainPanelController,self).__init__()
        self.layout = QHBoxLayout()
        self.DisplayModelsModel = None

    @Log.LogClassFuncInfos
    def InitGUI(self):
        pass

    @Log.LogClassFuncInfos
    def InitModel(self):
        self.DisplayModelsModel = DisplayModelsModel()

    @Log.LogClassFuncInfos
    def Update(self,model):
        pass

    @Log.LogClassFuncInfos
    def SetModel(self, model):
        if model.Name == self.DisplayModelsModel.Name:
            self.DisplayModelsModel.Name = model
            self.DisplayModelsModel.AddObserves(self)

    @Log.LogClassFuncInfos
    def SetLayout(self, layout):
        self.layout = layout


class DicomToolThumbnailController(DicomViewerBasePanelController,Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomToolThumbnailController,self).__init__()
        self.Name = 'DicomToolThumbnailController'
        self.listWidgets = []
        self.layout = QVBoxLayout()
        self.SequenceModel = SequenceModel()
        self.SequenceInfoModel = SequenceInfoModel()
        self.DisplayModelsModel = DisplayModelsModel()

    @Log.LogClassFuncInfos
    def InitGUI(self):
        pass

    @Log.LogClassFuncInfos
    def InitModel(self):
        pass

    @Log.LogClassFuncInfos
    def Update(self,model):
        if model.Name == self.SequenceInfoModel.Name:
            self.SequenceInfoChange()

    @Log.LogClassFuncInfos
    def updatePatient(self):
        SequenceInfos = self.SequenceInfoModel.GetSequenceInfo()
        if len(SequenceInfos.keys()) == 2:
            pass
        if len(SequenceInfos.keys()) is len(self.listWidgets):
            return
        patients = None
        if len(self.listWidgets) is 0:
            patients = list(SequenceInfos.keys())[0]
        for patientName in SequenceInfos.keys():
            for listWidget in self.listWidgets:
                if patientName is not listWidget.getPatientName():
                    patients = patientName

        if patients is not None:
            listWidget = ThumbnailListWidget()
            listWidget.setFocus()
            listWidget.itemClicked.connect(self.ThumbnialItemClick)
            listWidget.setPatientName(patients)
            listWidget.setContentsMargins(0, 0, 0, 0)
            # listWidget.verticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            listWidget.horizontalOffset()
            # listWidget.horizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # listWidget.horizontalScrollBar().setDisabled(True)
            listWidget.setFixedWidth(ParaSetting.ThumbnailWidgetWidth)
            listWidget.setStyleSheet("background-color: rgb(%d, %d, %d)"%(ParaSetting.ThumbnailWidgetColorR,
                                                                          ParaSetting.ThumbnailWidgetColorG,
                                                                          ParaSetting.ThumbnailWidgetColorB))
            self.layout.addWidget(listWidget)
            self.listWidgets.append(listWidget)

            dicomName = list(list(SequenceInfos[patients].values())[0].values())[0]
            reader = sitk.ImageFileReader()
            reader.SetFileName(dicomName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            patient_name = reader.GetMetaData(Tags['PatientName'])
            patient_birth = reader.GetMetaData(Tags['DataOfBirth'])

            patient_info = CharacterDisplayLabel()
            patient_info.setText('%s\t\n%s'%(patient_name,patient_birth))
            patient_info.setCharacterColor(Qt.white)
            patient_info.setBackgroundColor(ParaSetting.PatientNameDisplayColorR,
                                            ParaSetting.PatientNameDisplayColorG,
                                            ParaSetting.PatientNameDisplayColorB,255)

            patient_info_widgetItem = QListWidgetItem()

            # print(ParaSetting.ThumbnailPatientNameHeight, ParaSetting.ThumbnailWidgetWidth)
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

    @Log.LogClassFuncInfos
    def SequenceInfoChange(self):
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

    @Log.LogClassFuncInfos
    def SetModel(self, model):
        if model.Name is self.SequenceModel.Name:
            self.SequenceModel = model
            model.AddObserves(self)
        elif model.Name is self.SequenceInfoModel.Name:
            self.SequenceInfoModel = model
            model.AddObserves(self)
        elif model.Name is self.DisplayModelsModel.Name:
            self.DisplayModelsModel = model
            model.AddObserves(self)

    @Log.LogClassFuncInfos
    def SetLayout(self, layout):
        self.layout = layout

    @Log.LogClassFuncInfos
    def ThumbnialItemClick(self, item):

        listWidget = item.listWidget()
        curwidget = listWidget.itemWidget(item)

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            curwidget.setSelectState( not curwidget.getSelectState() )
        else:
            for listwidget in self.listWidgets:
                listwidget.setAllToNotSelected()
            curwidget.setSelectState(True)


class DicomToolPageController(Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomToolPageController,self).__init__()
        self.Name = 'DicomToolPageController'
        self.MainPanelController = DicomToolMainPanelController()
        self.ThumbnailControlelr = DicomToolThumbnailController()
        self.InitModel()

    @Log.LogClassFuncInfos
    def InitModel(self):
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

    @Log.LogClassFuncInfos
    def InitGUI(self):
        self.MainPanelController.InitGUI()
        self.ThumbnailControlelr.InitGUI()

    @Log.LogClassFuncInfos
    def SetModelDown(self):
        self.MainPanelController.SetModel(self.ImageNamesModel)
        self.ThumbnailControlelr.SetModel(self.ImageNamesModel)
        self.MainPanelController.SetModel(self.SequenceModel)
        self.ThumbnailControlelr.SetModel(self.SequenceModel)
        self.ThumbnailControlelr.SetModel(self.SequenceInfoModel)
        self.MainPanelController.SetModel(self.DisplayModelsModel)
        self.ThumbnailControlelr.SetModel(self.DisplayModelsModel)

    @Log.LogClassFuncInfos
    def SetLayout(self, layout):
        self.layout = layout
        thumbnailLayout = QVBoxLayout()
        mainPanalLayout = QVBoxLayout()

        self.layout.addLayout(thumbnailLayout)
        self.layout.addStretch()
        self.layout.addLayout(mainPanalLayout)
        self.MainPanelController.SetLayout(mainPanalLayout)
        self.ThumbnailControlelr.SetLayout(thumbnailLayout)

    @Log.LogClassFuncInfos
    def SetModel(self, model):
        if model.Name == 'ImageNamesModel':
            self.ImageNamesModel = model
            self.ImageNamesModel.AddObserves(self)


        self.SetModelDown()

    @Log.LogClassFuncInfos
    def Update(self,model):
        if model.Name == self.ImageNamesModel.Name:
            self.ImageNamesChange()

    @Log.LogClassFuncInfos
    def ImageNamesChange(self):
        ImageNames = self.ImageNamesModel.getImageNames()
        if ImageNames is None:
            return

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
        pass

if __name__ == '__main__':

    a = DicomToolPageController()
    b = DicomToolPageController()



