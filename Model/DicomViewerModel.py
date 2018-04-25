
from Model import BaseModel
from Model.BaseModel import *
import Controller.Log as Log

class ImageNamesModel(BaseModel):

    def __init__(self):
        super(ImageNamesModel, self).__init__()
        Log.LogTrace('DicomBasicPanZoomViewer, Init')
        self.Name = 'ImageNamesModel'
        self.names = []

    def setImageNames(self,names):
        if names is not self.names:
            self.names = names
            super(ImageNamesModel, self).Notify()



if __name__=='__main__':

    a = ImageNamesModel()
    a.setImageNames(1)
    a.setImageNames(1)

