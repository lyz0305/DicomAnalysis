
from Controller.Observe import *
from Controller.DicomViewerBaseController import *
from Model.DicomViewerModel import *
import SimpleITK as sitk
from Controller.TagName import Tags
from Viewer.DicomViewViewer import ThumbnailViewer
from Viewer.AuxiliaryClass import CharacterDisplayLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Controller import ParaSetting
from Controller import Log
from Controller import DicomViewerThread
import pydicom


class DicomToolViewController(DicomViewerBasePanelController, Observe):
    '''
    the dicom may display two or more image in the same time
    we need a controller to control each image
    '''
    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolViewController'
        super(DicomToolViewController, self).__init__()
        self.__layout = QHBoxLayout()
        self.__displayInfoModel = DisplayInfoModel()

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
        if model.Name is self.__displayInfoModel.Name:
            self.__displayInfoModel = model
            self.__displayInfoModel.AddObserves(self)

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
        self.__patientNames = []

    @Log.LogClassFuncInfos
    def initGUI(self):
        self.__listWidget = QListWidget()
        self.__listWidget.itemClicked.connect(self.thumbnialItemClick)
        self.__listWidget.setFocus()
        self.__listWidget.setHorizontalScrollMode(QListWidget.ScrollPerPixel)
        self.__listWidget.setContentsMargins(0, 0, 0, 0)
        self.__listWidget.setFixedWidth(ParaSetting.ThumbnailWidgetWidth)
        self.__listWidget.setStyleSheet("background-color: rgb(%d, %d, %d)" % (ParaSetting.ThumbnailWidgetColorR,
                                                                               ParaSetting.ThumbnailWidgetColorG,
                                                                               ParaSetting.ThumbnailWidgetColorB))

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__listWidget)
        pass

    @Log.LogClassFuncInfos
    def initModel(self):
        self.__sequenceModel = SequenceModel()
        self.__sequenceInfoModel = SequenceInfoModel()
        self.__displayModelsModel = DisplayModelsModel()

    @Log.LogClassFuncInfos
    def update(self,model):
        if model.Name == self.__sequenceInfoModel.Name:
            self.sequenceInfoChange()

    @Log.LogClassFuncInfos
    def findLocationOfPatient(self, patientName):
        start = -1
        end = -1
        N = self.__listWidget.count()
        for i in range(N):

            widgetItem = self.__listWidget.item(i)
            widget = self.__listWidget.itemWidget(widgetItem)

            if isinstance(widget, ThumbnailViewer):
                if patientName is widget.getPatientName():
                    end = i
            else:
                if widget.getProperty('patientName') is patientName:
                    start = i
                    end = i
        return start, end

    @Log.LogClassFuncInfos
    def findLocationOfSery(self, patientName, seryName):
        '''

        :param patientName:
        :param seryName:
        :return: the index of sery in the list
        '''
        index = -1
        start,end = self.findLocationOfPatient(patientName)

        for i in range(start+1,end+1):
            widgetItem = self.__listWidget.item(i)
            widget = self.__listWidget.itemWidget(widgetItem)
            if isinstance(widget, ThumbnailViewer):
                if seryName is widget.getSeryName():
                    index = i
                    return index
        return index

    @Log.LogClassFuncInfos
    def updatePatient(self):

        if self.__listWidget.count() is 0:
            self.__layout.addWidget(self.__listWidget)

        SequenceInfos = self.__sequenceInfoModel.getSequenceInfo()

        patient = None

        # if self.__listWidget.count() is 0:
        #     patient = list(SequenceInfos.keys())[0]

        for patientName in SequenceInfos.keys():

            if patientName not in self.__patientNames:
                patient = patientName
                self.__patientNames.append(patientName)
                break

        if patient is not None:

            dicomName = list(list(SequenceInfos[patient].values())[0].values())[0]
            reader = sitk.ImageFileReader()
            reader.SetFileName(dicomName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            patient_name = reader.GetMetaData(Tags['PatientName'])
            patient_birth = reader.GetMetaData(Tags['DataOfBirth'])

            patient_info = CharacterDisplayLabel()
            patient_info.setProperty('patientName', patientName)
            patient_info.setText('%s\t\n%s'%(patient_name,patient_birth))
            patient_info.setCharacterColor(Qt.white)
            patient_info.setBackgroundColor(ParaSetting.PatientNameDisplayColorR,
                                            ParaSetting.PatientNameDisplayColorG,
                                            ParaSetting.PatientNameDisplayColorB,255)

            patient_info_widgetItem = QListWidgetItem()
            patient_info_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailWidgetWidth, ParaSetting.ThumbnailPatientNameHeight))
            self.__listWidget.insertItem(self.__listWidget.count(), patient_info_widgetItem)
            self.__listWidget.setItemWidget(patient_info_widgetItem, patient_info)


    @Log.LogClassFuncInfos
    def sequenceInfoChange(self):
        SequenceInfos = self.__sequenceInfoModel.getSequenceInfo()
        self.updatePatient()
        for patientName in SequenceInfos.keys():
            for seryName in SequenceInfos[patientName].keys():
                index = self.findLocationOfSery(patientName, seryName)
                if index is not -1:
                    # index is -1 means that we can not find the sery in the list
                    # index is not -1 means the list has had the sery
                    continue
                # since we can not find the sery in the list,
                # we insert the sery the last of the patient
                index = self.findLocationOfSery(patientName, seryName)
                start, end = self.findLocationOfPatient(patientName)

                thum = ThumbnailViewer()
                thum.setSeryName(seryName)
                thum.setPatientName(patientName)
                thum_widgetItem = QListWidgetItem()
                thum_widgetItem.setSizeHint(QSize(ParaSetting.ThumbnailWidgetWidth, ParaSetting.ThumbnailViewHeight))
                self.__listWidget.insertItem(end + 1, thum_widgetItem)
                self.__listWidget.setItemWidget(thum_widgetItem, thum)

                self.showAllImage()

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
        # self.__layout.addWidget(self.__listWidget)

    @Log.LogClassFuncInfos
    def thumbnialItemClick(self, item):

        listWidget = item.listWidget()
        curwidget = listWidget.itemWidget(item)

        if not isinstance(curwidget, ThumbnailViewer):
            return

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            curwidget.setSelectState( not curwidget.getSelectState() )
        else:
            # for listwidget in self.__listWidgets:
            #     listwidget.setAllToNotSelected()

            for i in range(self.__listWidget.count()):
                widgetItem = self.__listWidget.item(i)
                widget = self.__listWidget.itemWidget(widgetItem)
                if isinstance(widget, ThumbnailViewer):
                    widget.setSelectState(False)
            curwidget.setSelectState(True)

    @Log.LogClassFuncInfos
    def showAllImage(self):

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()

        for i in range(self.__listWidget.count()):

            widgetItem = self.__listWidget.item(i)
            widget = self.__listWidget.itemWidget(widgetItem)
            if isinstance(widget, ThumbnailViewer):
                patientName = widget.getPatientName()
                seryName = widget.getSeryName()
                images = sequenceInfo[patientName][seryName]

                instance = list(images.keys())
                instance.sort()
                midInstance = instance[len(instance)//2]
                imgPath = images[midInstance]
                # imgPath = images[instance[0]]
                ds = pydicom.dcmread(imgPath)
                img = ds.pixel_array
                widget.setImage(img)

        # for listWidget in self.__listWidgets:
        #     N = listWidget.count()
        #     patientName = listWidget.getPatientName()
        #     for i in range(N):
        #         widgetItem = listWidget.item(i)
        #         widget = listWidget.itemWidget(widgetItem)
        #         if isinstance(widget, ThumbnailViewer):
        #             seryName = widget.getSeriesName()
        #             images = sequenceInfo[patientName][seryName]
        #
        #             instance = list(images.keys())
        #             instance.sort()
        #             midInstance = instance[len(instance)//2]
        #             imgPath = images[midInstance]
        #             # imgPath = images[instance[0]]
        #             ds = pydicom.dcmread(imgPath)
        #             img = ds.pixel_array
        #             widget.setImage(img)




class DicomToolPageController(Observe):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomToolPageController,self).__init__()
        self.Name = 'DicomToolPageController'
        self.__mainPanelController = DicomToolMainPanelController()
        self.__thumbnailControlelr = DicomToolThumbnailController()
        self.__statusController = DicomStatusController()
        self.__dicomViewControllerLists = []
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
    def addDicomView(self, patienName, seryName):
        pass

    @Log.LogClassFuncInfos
    def allDicomHeaderRead(self):
        self.__thumbnailControlelr.showAllImage()
        self.__statusController.setText('%d/%d' %(len(self.__imageNamesModel.getImageNames()), len(self.__imageNamesModel.getImageNames())))


        # displayInfoModel = DisplayInfoModel()
        # sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        # patientName = list(sequenceInfo.keys())[0]
        # seryName = list(sequenceInfo[patientName].keys())[0]
        #
        # images = sequenceInfo[patientName][seryName]
        # instance = list(images.keys())
        # instance.sort()
        # midInstance = instance[len(instance) // 2]
        #
        # displayInfoModel.setDisplayInfo(patientName,seryName,midInstance)
        # dicomToolViewController = DicomToolViewController()
        # self.__dicomViewControllerLists.append(dicomToolViewController)




if __name__ == '__main__':

    a = DicomToolPageController()
    b = DicomToolPageController()



