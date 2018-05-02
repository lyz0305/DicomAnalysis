
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
from Viewer.DicomBasicPanZoomViewer import DicomBasicPanZoomViewer
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

    @Log.LogClassFuncInfos
    def initGUI(self):
        self.__layout = QHBoxLayout()
        self.__imgView = QLabel()
        self.__sequenceInfoModel = SequenceInfoModel()

        self.__imgView = DicomBasicPanZoomViewer()
        self.__imgView.setModel(self.__displayInfoModel)


        self.__scrollBar = QScrollBar()
        self.__scrollBar.valueChanged.connect(self.scrollSliderChange)

    @Log.LogClassFuncInfos
    def getModel(self, name):

        if self.__displayInfoModel.Name is name:
            return self.__displayInfoModel

        return None

    @Log.LogClassFuncInfos
    def initModel(self):
        self.__displayInfoModel = DisplayInfoModel()

    @Log.LogClassFuncInfos
    def update(self,model):

        if model.Name is self.__displayInfoModel.Name:
            self.instanceNumberChange()

    @Log.LogClassFuncInfos
    def instanceNumberChange(self):

        changes = self.__displayInfoModel.getInstanceChange()
        patientName = self.__displayInfoModel.getPatientName()
        seryName = self.__displayInfoModel.getSeryName()
        ori_instance = self.__displayInfoModel.getInstanceNumber()

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        sery = sequenceInfo[patientName][seryName]
        instanceNumbers = list(sery.keys())
        instanceNumbers.sort()

        if changes == ParaSetting.SeryChange:
            instance = instanceNumbers[0]
        else:
            index = instanceNumbers.index(ori_instance)
            cur_instance = index + changes
            if cur_instance >= len(instanceNumbers):
                instance = instanceNumbers[-1]
            elif cur_instance < 0:
                instance = instanceNumbers[0]
            else:
                instance = instanceNumbers[cur_instance]

        self.__displayInfoModel.setInstanceNumber(instance)
        self.__scrollBar.setValue(instanceNumbers.index(instance))

        imgPath = sequenceInfo[patientName][seryName][instance]

        ds = pydicom.dcmread(imgPath)
        img = ds.pixel_array
        img = img.astype(float) * ds.RescaleSlope + ds.RescaleIntercept
        self.__imgView.setImage(img)
        center, width = self.__imgView.getContrast()
        x,y = self.__imgView.getPan()

        # self.__imgView.contrastLabelPan(x,y)
        # self.__imgView.setContrast(center=center, width=width)

    @Log.LogClassFuncInfos
    def setModel(self, model):
        if model.Name is self.__displayInfoModel.Name:
            self.__displayInfoModel = model
            self.__displayInfoModel.AddObserves(self)
        elif model.Name is self.__sequenceInfoModel.Name:
            self.__sequenceInfoModel = model

    @Log.LogClassFuncInfos
    def initDisplay(self):

        model = self.__displayInfoModel
        patientName = model.getPatientName()
        seryName = model.getSeryName()
        instanceNum = model.getInstanceNumber()

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        imgPath = sequenceInfo[patientName][seryName][instanceNum]
        ds = pydicom.dcmread(imgPath)
        img = ds.pixel_array
        img = img.astype(float)*ds.RescaleSlope + ds.RescaleIntercept

        layout = QHBoxLayout()


        self.__imgView.setImage(img)
        self.__imgView.resetContrast()
        self.__imgView.setModel(self.__displayInfoModel)

    @Log.LogClassFuncInfos
    def getImageView(self):
        return self.__imgView

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        self.__layout = layout
        # self.__layout.addWidget(self.__imgView)

        layout = QHBoxLayout()
        layout.addWidget(self.__imgView)
        layout.addWidget(self.__scrollBar)
        self.__layout.addLayout(layout)

    @Log.LogClassFuncInfos
    def seryChange(self, patientName, seryName):
        self.__displayInfoModel.setDisplayInfo(patientName, seryName, None)
        self.__displayInfoModel.instanceChange(ParaSetting.SeryChange)

    @Log.LogClassFuncInfos
    def imageNumberChange(self):
        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        patientName = self.__displayInfoModel.getPatientName()
        seryName = self.__displayInfoModel.getSeryName()
        sery = sequenceInfo[patientName][seryName]
        instanceNumbers = list(sery.keys())
        self.__scrollBar.setRange(0, len(instanceNumbers)-1)
        self.__scrollBar.setSingleStep(1)



    @Log.LogClassFuncInfos
    def scrollSliderChange(self, val):

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        patientName = self.__displayInfoModel.getPatientName()
        seryName = self.__displayInfoModel.getSeryName()
        instanceNumber = self.__displayInfoModel.getInstanceNumber()
        sery = sequenceInfo[patientName][seryName]
        instanceNumbers = list(sery.keys())
        instanceNumbers.sort()
        index = instanceNumbers.index(instanceNumber)
        change = val - index
        self.__displayInfoModel.instanceChange(change)

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
        self.__activeViewController = None

    @Log.LogClassFuncInfos
    def setActiveViewController(self, controller):
        self.__activeViewController = controller

    @Log.LogClassFuncInfos
    def getActiveViewContrller(self):
        return self.__activeViewController

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

                if len(self.__displayModelsModel.getDisplayModels()) is 0:

                    displayInfo = DisplayInfoModel()
                    instanceNumbers = list(SequenceInfos[patientName][seryName].keys())
                    instanceNumbers.sort()
                    displayInfo.setDisplayInfo(patientName, seryName, instanceNumbers[0])

                    self.__displayModelsModel.addDisplayModels(displayInfo)

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
            # model.AddObserves(self)

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

        self.__activeViewController.seryChange(curwidget.getPatientName(), curwidget.getSeryName())

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
        self.__thumbnailController = DicomToolThumbnailController()
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
        self.__displayModelsModel.AddObserves(self)

        self.__thumbnailController.initModel()
        self.setModelDown()

    @Log.LogClassFuncInfos
    def initGUI(self):

        self.__thumbnailController.InitGUI()

    @Log.LogClassFuncInfos
    def setModelDown(self):
        self.__thumbnailController.setModel(self.__imageNamesModel)
        self.__thumbnailController.setModel(self.__sequenceModel)
        self.__thumbnailController.setModel(self.__sequenceInfoModel)
        self.__thumbnailController.setModel(self.__displayModelsModel)

    @Log.LogClassFuncInfos
    def setLayout(self, layout):
        self.layout = layout

        mainLayout = QHBoxLayout()
        thumbnailLayout = QVBoxLayout()
        mainPanalLayout = QVBoxLayout()
        mainLayout.addLayout(thumbnailLayout)
        mainLayout.addLayout(mainPanalLayout)

        statusLabel = QLabel()


        self.layout.addLayout(mainLayout)
        self.layout.addWidget(statusLabel,0,Qt.AlignBottom)
        self.__thumbnailController.setLayout(thumbnailLayout)
        self.__statusController.setLabel(statusLabel)

        self.__mainViewLayout = mainPanalLayout

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
        elif model.Name == self.__displayModelsModel.Name:
            self.numberOfDisplayChange()

    @Log.LogClassFuncInfos
    def numberOfDisplayChange(self):

        displayModels = self.__displayModelsModel.getDisplayModels()

        model = None
        # to find the new model
        for displayModel in displayModels:
            Exist = False
            for viewController in self.__dicomViewControllerLists:
                if viewController.getModel( displayModels.Name ) is displayModel:
                    Exist = True
                    break
            if Exist is False:
                model = displayModel
                break

        if model is None:
            return

        dicomToolViewController = DicomToolViewController()
        dicomToolViewController.setModel(model)
        dicomToolViewController.setModel(self.__sequenceInfoModel)
        dicomToolViewController.initDisplay()

        if len(self.__dicomViewControllerLists) is 0:
            self.__thumbnailController.setActiveViewController(dicomToolViewController)

        self.__dicomViewControllerLists.append(dicomToolViewController)

        # currently, only one image can be display
        if len(displayModels) == 1:

            # imgView = dicomToolViewController.getImageView()
            layout = QHBoxLayout()
            dicomToolViewController.setLayout(layout)
            self.__mainViewLayout.addLayout(layout)
            pass

    @Log.LogClassFuncInfos
    def imageNamesChange(self):
        ImageNames = self.__imageNamesModel.getImageNames()
        if ImageNames is None:
            return

        sequenceInfo = self.__sequenceInfoModel.getSequenceInfo()
        N = len(ImageNames)
        reader = sitk.ImageFileReader()

        for i in range(N):
            dcmName = ImageNames[i]
            reader.SetFileName(dcmName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            series_description = reader.GetMetaData(Tags['SeriesDescription'])
            series_number = reader.GetMetaData(Tags['SeriesNumber'])
            instance_number = int(reader.GetMetaData(Tags['InstanceNumber']))
            patient_name = reader.GetMetaData(Tags['PatientName'])
            seryName = series_number + ' ' + series_description

            self.aDicomHeaderRead(patientName=patient_name, seryName=seryName, instanceNumber=instance_number, path=dcmName)
            QCoreApplication.processEvents()

        self.allDicomHeaderRead()

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
        self.__thumbnailController.getActiveViewContrller().imageNumberChange()

    @Log.LogClassFuncInfos
    def addDicomView(self, patienName, seryName):
        pass

    @Log.LogClassFuncInfos
    def allDicomHeaderRead(self):
        self.__thumbnailController.showAllImage()
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



