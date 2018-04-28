
from Model import BaseModel
from Model.BaseModel import *
import Controller.Log as Log

class ImageNamesModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(ImageNamesModel, self).__init__()
        self.Name = 'ImageNamesModel'
        self.names = []

    @Log.LogClassFuncInfos
    def setImageNames(self,names):
        if names is not self.names:
            self.names = names
            self.Notify()

    @Log.LogClassFuncInfos
    def getImageNames(self):
        return self.names

class SequenceModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(SequenceModel,self).__init__()
        self.Name = 'SequenceModel'
        self.Sequence = dict()

    @Log.LogClassFuncInfos
    def SetSequence(self, Sequence):
        if Sequence is not self.Sequence:
            self.Sequence = Sequence
            self.Notify()

    @Log.LogClassFuncInfos
    def GetSequence(self):
        return self.SequenceList

class SequenceInfoModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(SequenceInfoModel,self).__init__()
        self.Name = 'SequenceInfoModel'
        self.SequenceInfo = dict()

    @Log.LogClassFuncInfos
    def SetSequenceInfo(self,Info):
        if Info is not self.SequenceInfo:
            self.SequenceInfo = Info
            self.Notify()

    @Log.LogClassFuncInfos
    def GetSequenceInfo(self):
        return self.SequenceInfo.copy()

class DisplayImageModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DisplayImageModel, self).__init__()
        self.Name = 'DisplayImageModel'
        self.Img = None

    @Log.LogClassFuncInfos
    def setImage(self, image):
        if image is not self.Img:
            self.Img = image
            self.Notify()

    @Log.LogClassFuncInfos
    def getImage(self):
        return self.Img


class DisplayInfoModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DisplayInfoModel,self).__init__()
        self.Name = 'DisplayInfoModel'
        self.patientName = None
        self.seriesName = None
        self.instanceNumber = None

    @Log.LogClassFuncInfos
    def setDisplayInfo(self, patientName, seriesName, instanceNumber):
        if patientName is not self.patientName or seriesName is not self.seriesName\
                or instanceNumber is not self.instanceNumber:
            self.patientName = patientName
            self.seriesName = seriesName
            self.instanceNumber = instanceNumber
            self.Notify()

    @Log.LogClassFuncInfos
    def getPatientName(self):
        return self.patientName

    @Log.LogClassFuncInfos
    def getSeriesName(self):
        return self.seriesName

    @Log.LogClassFuncInfos
    def getInstanceNumber(self):
        return self.instanceNumber

class DisplayModelsModel(BaseModel):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DisplayModelsModel, self).__init__()
        self.Name = 'DisplayModelModel'
        self.DisplayModels = []

    @Log.LogClassFuncInfos
    def setDisplayModels(self, models):
        if models is not self.DisplayModels:
            self.DisplayModels = models
            self.Notify()

    @Log.LogClassFuncInfos
    def getDisplayModels(self):
        return self.DisplayModels

if __name__=='__main__':

    a = ImageNamesModel()
    a.setImageNames(1)
    a.setImageNames(1)

