
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



class DisplayIDModel(BaseModel):
    def __init__(self):
        Log.LogTrace('DisplayIDModel, Init')
        super(DisplayIDModel,self).__init__()
        self.Name = 'DisplayIDModel'
        self.ID = []
    def SetID(self, ID):
        Log.LogTrace('DisplayIDModel, SetID')
        if ID is not self.ID:
            self.ID = ID
            self.Notify()
    def GetID(self, ID):
        Log.LogTrace('DisplayIDModel, GetID')
        return self.ID


if __name__=='__main__':

    a = ImageNamesModel()
    a.setImageNames(1)
    a.setImageNames(1)

