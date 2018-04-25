
from Controller.Log import *
import sys

class DicomToolBasePanelController:

    def __init__(self):
        LogTrace('DicomToolBaseController, Init')
        self.Name = 'DicomToolBasePanelController'
        self.InitGUI()
        self.InitModel()

    def InitModel(self):
        LogTrace('DicomToolBaseController, InitModel')
        sys.exit('Controller must rewrite the InitModel function')

    def InitGUI(self):
        LogTrace('DicomToolBaseController, InitGUI')
        sys.exit('Controller must rewrite the InitGUI function')

    def SetModel(self, model):
        LogTrace('DicomToolBaseController, SetModel')
        sys.exit('Controller must rewrite the SetModel function')

    def Update(self, model):
        LogTrace('DicomToolBaseController, Update')
        sys.exit('Controller must rewrite the Update function')