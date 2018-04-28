
from Controller import Log
import sys

class DicomViewerBasePanelController:

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolBasePanelController'
        self.InitGUI()
        self.InitModel()

    @Log.LogClassFuncInfos
    def InitModel(self):
        sys.exit('Controller must rewrite the InitModel function')

    @Log.LogClassFuncInfos
    def InitGUI(self):
        sys.exit('Controller must rewrite the InitGUI function')

    @Log.LogClassFuncInfos
    def SetModel(self, model):
        sys.exit('Controller must rewrite the SetModel function')

    @Log.LogClassFuncInfos
    def Update(self, model):
        sys.exit('Controller must rewrite the Update function')