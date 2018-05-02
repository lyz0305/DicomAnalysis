
from Model import BaseModel
from Model.BaseModel import *
import Controller.Log as Log

class ImageNamesModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(ImageNamesModel, self).__init__()
        self.Name = 'ImageNamesModel'
        self.__names = []

    @Log.LogClassFuncInfos
    def setImageNames(self,names):
        if names is not self.__names:
            self.__names = names
            self.Notify()

    @Log.LogClassFuncInfos
    def getImageNames(self):
        return self.__names

class SequenceModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(SequenceModel,self).__init__()
        self.Name = 'SequenceModel'
        self.__Sequence = dict()

    @Log.LogClassFuncInfos
    def setSequence(self, Sequence):
        if Sequence is not self.__Sequence:
            self.__Sequence = Sequence
            self.Notify()

    @Log.LogClassFuncInfos
    def getSequence(self):
        return self.__Sequence

class SequenceInfoModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(SequenceInfoModel,self).__init__()
        self.__sequenceInfo = dict()

    @Log.LogClassFuncInfos
    def setSequenceInfo(self,Info):
        if Info is not self.__sequenceInfo:
            self.__sequenceInfo = Info
            self.Notify()

    @Log.LogClassFuncInfos
    def getSequenceInfo(self):
        return self.__sequenceInfo.copy()

class AddImageInfoModel(BaseModel):
    '''
    when a more image need to be shown, a more DisplayInfoModel would be created
    then, the AddImageInfoModel would be change
    '''
    @Log.LogClassFuncInfos
    def __init__(self):
        super(AddImageInfoModel, self).__init__()
        self.__displayInfoModel = None

    @Log.LogClassFuncInfos
    def setDisplayInfoModel(self, displayInfoModel):
        if displayInfoModel is not self.__displayInfoModel:
            self.__displayInfoModel = displayInfoModel

    @Log.LogClassFuncInfos
    def getDisplayInfoModel(self):
        return self.__displayInfoModel

class DisplayInfoModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DisplayInfoModel,self).__init__()
        self.Name = 'DisplayInfoModel'
        self.__patientName = None
        self.__seryName = None
        self.__instanceNumber = None
        self.__numChange = 0

    @Log.LogClassFuncInfos
    def setDisplayInfo(self, patientName, seriesName, instanceNumber):
        if patientName is not self.__patientName or seriesName is not self.__seryName\
                or instanceNumber is not self.__instanceNumber:
            self.__patientName = patientName
            self.__seryName = seriesName
            self.__instanceNumber = instanceNumber
            # self.Notify()

    @Log.LogClassFuncInfos
    def instanceChange(self, num):
        if num is not 0:
            self.__numChange = num
            self.Notify()

    @Log.LogClassFuncInfos
    def getInstanceChange(self):
        return self.__numChange

    @Log.LogClassFuncInfos
    def getPatientName(self):
        return self.__patientName

    @Log.LogClassFuncInfos
    def getSeryName(self):
        return self.__seryName

    @Log.LogClassFuncInfos
    def getInstanceNumber(self):
        return self.__instanceNumber

    @Log.LogClassFuncInfos
    def setInstanceNumber(self, instance):
        self.__instanceNumber = instance

class DisplayModelsModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DisplayModelsModel, self).__init__()
        self.Name = 'DisplayModelModel'
        self.__displayModels = []

    @Log.LogClassFuncInfos
    def setDisplayModels(self, models):
        if models is not self.__displayModels:
            self.__displayModels = models
            self.Notify()

    @Log.LogClassFuncInfos
    def getDisplayModels(self):
        return self.__displayModels

    @Log.LogClassFuncInfos
    def addDisplayModels(self,model):
        self.__displayModels.append(model)
        self.Notify()

if __name__=='__main__':

    a = ImageNamesModel()
    a.setImageNames(1)
    a.setImageNames(1)

