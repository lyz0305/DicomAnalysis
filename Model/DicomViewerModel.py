
from Model import BaseModel
from Model.BaseModel import *
import Controller.Log as Log

class ImageNamesModel(BaseModel):

    def __init__(self):
        Log.LogTrace('ImageNamesModel, Init')
        super(ImageNamesModel, self).__init__()
        self.Name = 'ImageNamesModel'
        self.names = []

    def SetImageNames(self,names):
        Log.LogTrace('ImageNamesModel, SetImageNames')
        if names is not self.names:
            self.names = names
            self.Notify()

    def GetImageNames(self):
        Log.LogTrace('ImageNamesModel, GetImageNames')
        return self.names

class SequenceModel(BaseModel):
    def __init__(self):
        Log.LogTrace('SequenceModel, Init')
        super(SequenceModel,self).__init__()
        self.Name = 'SequenceModel'
        self.Sequence = dict()

    def SetSequence(self, Sequence):
        Log.LogTrace('SequenceModel, SetSequence')
        if Sequence is not self.Sequence:
            self.Sequence = Sequence
            self.Notify()
    def GetSequence(self):
        Log.LogTrace('SequenceModel, GetSequence')
        return self.SequenceList

class SequenceInfoModel(BaseModel):
    def __init__(self):
        Log.LogTrace('SequenceInfoModel, Init')
        super(SequenceInfoModel,self).__init__()
        self.Name = 'SequenceInfoModel'
        self.SequenceInfo = dict()

    def SetSequenceInfo(self,Info):
        Log.LogTrace('SequenceInfoModel,SetSequenceInfo')
        if Info is not self.SequenceInfo:
            self.SequenceInfo = Info
            self.Notify()

    def GetSequenceInfo(self):
        Log.LogTrace('SequenceInfoModel,GetSequenceInfo')
        return self.SequenceInfo.copy()

class DisplayImageModel(BaseModel):
    def __init__(self):
        Log.LogTrace('DisplayImageModel, Init')
        super(DisplayImageModel, self).__init__()
        self.Name = 'DisplayImageModel'
        self.Img = None

    def setImage(self, image):
        Log.LogTrace('DisplayImageModel, setImage')
        if image is not self.Img:
            self.Img = image
            self.Notify()

    def getImage(self):
        Log.LogTrace('DisplayImageModel, getImage')
        return self.Img


class DisplayInfoModel(BaseModel):
    def __init__(self):
        Log.LogTrace('DisplayInfoModel, Init')
        super(DisplayInfoModel,self).__init__()
        self.Name = 'DisplayInfoModel'
        self.patientName = None
        self.seriesName = None
        self.instanceNumber = None

    def setDisplayInfo(self, patientName, seriesName, instanceNumber):
        Log.LogTrace('DisplayInfoModel, setDisplayInfo')
        if patientName is not self.patientName or seriesName is not self.seriesName\
                or instanceNumber is not self.instanceNumber:
            self.patientName = patientName
            self.seriesName = seriesName
            self.instanceNumber = instanceNumber
            self.Notify()

    def getPatientName(self):
        LogTrace('DisplayInfoModel, getPatientName')
        return self.patientName

    def getSeriesName(self):
        LogTrace('DisplayIDModel, getSeriesName')
        return self.seriesName

    def getInstanceNumber(self):
        LogTrace('DisplayIDModel, getInstanceNumber')
        return self.instanceNumber

class DisplayModelsModel(BaseModel):

    def __init__(self):
        Log.LogTrace('DisplayModelModel, Init')
        super(DisplayModelsModel, self).__init__()
        self.Name = 'DisplayModelModel'
        self.DisplayModels = []

    def setDisplayModels(self, models):
        Log.LogTrace('DisplayModelModel, setDisplayModels')
        if models is not self.DisplayModels:
            self.DisplayModels = models
            self.Notify()

    def getDisplayModels(self):
        Log.LogTrace('DisplayModelModel, getDisplayModels')
        return self.DisplayModels

if __name__=='__main__':

    a = ImageNamesModel()
    a.setImageNames(1)
    a.setImageNames(1)

