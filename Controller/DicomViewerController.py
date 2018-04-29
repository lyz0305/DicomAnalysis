
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
from Controller import DicomViewerThread
import pydicom


class DicomToolViewController(DicomViewerBasePanelController, Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolViewController'
        super(DicomToolViewController, self).__init__()
        self.__layout = QHBoxLayout()

    @Log.LogClassFuncInfos
    def initGUI(self):
        pass

    @Log.LogClassFuncInfos
    def initModel(self):
        pass

    @Log.LogClassFuncInfos
    def update(self,model):
        pass

    @Log.LogClassFuncInfos
    def setModel(self, model):
        pass

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        pass
        self.layout = layout

class DicomToolMainPanelController(DicomViewerBasePanelController, Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolMainPanelController'
        super(DicomToolMainPanelController,self).__init__()
        self.__layout = QHBoxLayout()
        self.__displayModelsModel = None

    @Log.LogClassFuncInfos
    def initGUI(self):
        pass

    @Log.LogClassFuncInfos
    def initModel(self):
        self.__displayModelsModel = DisplayModelsModel()

    @Log.LogClassFuncInfos
    def update(self,model):
        pass

    @Log.LogClassFuncInfos
    def setModel(self, model):
        if model.Name == self.__displayModelsModel.Name:
            self.__displayModelsModel.Name = model
            self.__displayModelsModel.AddObserves(self)

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        self.layout = layout

class DicomStatusController:

    @Log.LogClassFuncInfos
    def __init__(self):
        self.__label = None


    @Log.LogClassFuncInfos
    def setLabel(self, layout):
        self.__label = layout

        self.__label.setMaximumHeight(30)
        self.__label.setStyleSheet("background-color: rgb(%d, %d, %d)"%(ParaSetting.StatusColorR,
                                                                        ParaSetting.StatusColorG,
                                                                        ParaSetting.StatusColorB))

    @Log.LogClassFuncInfos
    def setText(self, str):
        self.__label.setText(str)

class DicomToolThumbnailController(DicomViewerBasePanelController,Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomToolThumbnailController,self).__init__()
        self.Name = 'DicomToolThumbnailController'
        self.__listWidgets = []
        self.__layout = QVBoxLayout()
        self.__sequenceModel = SequenceModel()
        self.__sequenceInfoModel = SequenceInfoModel()
        self.__displayModelsModel = DisplayModelsModel()

    @Log.LogClassFuncInfos
    def initGUI(self):
        pass

    @Log.LogClassFuncInfos
    def initModel(self):
        pass

    @Log.LogClassFuncInfos
    def update(self,model):
        if model.Name == self.__sequenceInfoModel.Name:
            self.sequenceInfoChange()

    @Log.LogClassFuncInfos
    def updatePatient(self):
        SequenceInfos = self.__sequenceInfoModel.getSequenceInfo()
        # if len(SequenceInfos.keys()) == 2:
        #     pass
        if len(SequenceInfos.keys()) is len(self.__listWidgets):
            return
        patients = None
        if len(self.__listWidgets) is 0:
            patients = list(SequenceInfos.keys())[0]
        for patientName in SequenceInfos.keys():
            for listWidget in self.__listWidgets:
                if patientName is not listWidget.getPatientName():
                    patients = patientName

        if patients is not None:
            listWidget = ThumbnailListWidget()
            listWidget.setFocus()
            listWidget.itemClicked.connect(self.thumbnialItemClick)
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
            self.__layout.addWidget(listWidget)
            self.__listWidgets.append(listWidget)

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
    def sequenceInfoChange(self):
        SequenceInfos = self.__sequenceInfoModel.getSequenceInfo()
        self.updatePatient()
        for patientName in SequenceInfos.keys():
            for listWidget in self.__listWidgets:

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
    def setModel(self, model):
        if model.Name is self.__sequenceModel.Name:
            self.__sequenceModel = model
            model.AddObserves(self)
        elif model.Name is self.__sequenceInfoModel.Name:
            self.__sequenceInfoModel = model
            model.AddObserves(self)
        elif model.Name is self.__displayModelsModel.Name:
            self.__displayModelsModel = model
            model.AddObserves(self)

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        self.__layout = layout

    @Log.LogClassFuncInfos
    def thumbnialItemClick(self, item):

        listWidget = item.listWidget()
        curwidget = listWidget.itemWidget(item)

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            curwidget.setSelectState( not curwidget.getSelectState() )
        else:
            for listwidget in self.__listWidgets:
                listwidget.setAllToNotSelected()
            curwidget.setSelectState(True)

    @Log.LogClassFuncInfos
    def showAllImage(self):

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        for listWidget in self.__listWidgets:
            N = listWidget.count()
            patientName = listWidget.getPatientName()
            for i in range(N):
                widgetItem = listWidget.item(i)
                widget = listWidget.itemWidget(widgetItem)
                if isinstance(widget, ThumbnailViewer):
                    seryName = widget.getSeriesName()
                    images = sequenceInfo[patientName][seryName]

                    instance = list(images.keys())
                    instance.sort()
                    midInstance = instance[len(instance)//2]
                    midImgPath = images[midInstance]
                    ds = pydicom.dcmread(midImgPath)
                    img = ds.pixel_array
                    widget.setImage(img)




class DicomToolPageController(Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomToolPageController,self).__init__()
        self.Name = 'DicomToolPageController'
        self.__mainPanelController = DicomToolMainPanelController()
        self.__thumbnailControlelr = DicomToolThumbnailController()
        self.__statusController = DicomStatusController()
        self.__numberReadDicomHeader = 0
        self.initModel()

    @Log.LogClassFuncInfos
    def initModel(self):
        self.__imageNamesModel = ImageNamesModel()
        self.__sequenceModel = SequenceModel()
        self.__sequenceInfoModel = SequenceInfoModel()
        self.__displayModelsModel = DisplayModelsModel()

        self.__imageNamesModel.AddObserves(self)
        self.__sequenceModel.AddObserves(self)
        # self.SequenceInfoModel.AddObserves(self)

        self.__mainPanelController.initModel()
        self.__thumbnailControlelr.initModel()
        self.setModelDown()

    @Log.LogClassFuncInfos
    def initGUI(self):
        self.__mainPanelController.InitGUI()
        self.__thumbnailControlelr.InitGUI()

    @Log.LogClassFuncInfos
    def setModelDown(self):
        self.__mainPanelController.setModel(self.__imageNamesModel)
        self.__thumbnailControlelr.setModel(self.__imageNamesModel)
        self.__mainPanelController.setModel(self.__sequenceModel)
        self.__thumbnailControlelr.setModel(self.__sequenceModel)
        self.__thumbnailControlelr.setModel(self.__sequenceInfoModel)
        self.__mainPanelController.setModel(self.__displayModelsModel)
        self.__thumbnailControlelr.setModel(self.__displayModelsModel)

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        self.layout = layout

        mainLayout = QVBoxLayout()
        thumbnailLayout = QVBoxLayout()
        mainPanalLayout = QVBoxLayout()
        mainLayout.addLayout(thumbnailLayout)
        mainLayout.addLayout(mainPanalLayout)

        statusLabel = QLabel()


        self.layout.addLayout(mainLayout)
        self.layout.addWidget(statusLabel,0,Qt.AlignBottom)
        self.__mainPanelController.setLayout(mainPanalLayout)
        self.__thumbnailControlelr.setLayout(thumbnailLayout)
        self.__statusController.setLabel(statusLabel)

    @Log.LogClassFuncInfos
    def setModel(self, model):
        if model.Name == 'ImageNamesModel':
            self.__imageNamesModel = model
            self.__imageNamesModel.AddObserves(self)


        self.setModelDown()

    @Log.LogClassFuncInfos
    def update(self,model):
        if model.Name == self.__imageNamesModel.Name:
            self.imageNamesChange()

    @Log.LogClassFuncInfos
    def imageNamesChange(self):
        ImageNames = self.__imageNamesModel.getImageNames()
        if ImageNames is None:
            return

        self.__thread = DicomViewerThread.DicomHeaderReaderThread()
        self.__thread.setSequenceInfo(self.__sequenceInfoModel.getSequenceInfo())
        self.__thread.aDicomFinishConnect(self.aDicomHeaderRead)
        self.__thread.allDicomFinishConnect(self.allDicomHeaderRead)
        self.__thread.setImageNames(ImageNames)
        self.__thread.start()
        pass

    @Log.LogClassFuncInfos
    def aDicomHeaderRead(self, patientName, seryName, instanceNumber, path):
        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        if patientName not in sequenceInfo.keys():
            sequenceInfo[patientName] = dict()
        if seryName not in sequenceInfo[patientName].keys():
            sequenceInfo[patientName][seryName] = dict()
        sequenceInfo[patientName][seryName][instanceNumber] = path
        self.__sequenceInfoModel.setSequenceInfo(sequenceInfo)
        self.__numberReadDicomHeader = self.__numberReadDicomHeader + 1
        self.__statusController.setText('%d/%d'%(self.__numberReadDicomHeader, len(self.__imageNamesModel.getImageNames())))

    @Log.LogClassFuncInfos
    def allDicomHeaderRead(self):
        self.__thumbnailControlelr.showAllImage()
        self.__statusController.setText('%d/%d' %(len(self.__imageNamesModel.getImageNames()), len(self.__imageNamesModel.getImageNames())))


if __name__ == '__main__':

    a = DicomToolPageController()
    b = DicomToolPageController()



