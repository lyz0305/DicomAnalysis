
from Controller import Log
import sys

class DicomViewerBasePanelController:

    @Log.LogClassFuncInfos
    def __init__(self):
        self.Name = 'DicomToolBasePanelController'
        self.initGUI()
        self.initModel()

    @Log.LogClassFuncInfos
    def initModel(self):
        sys.exit('Controller must rewrite the InitModel function')

    @Log.LogClassFuncInfos
    def initGUI(self):
        sys.exit('Controller must rewrite the InitGUI function')

    @Log.LogClassFuncInfos
    def setModel(self, model):
        sys.exit('Controller must rewrite the SetModel function')

    @Log.LogClassFuncInfos
    def update(self, model):
        sys.exit('Controller must rewrite the Update function')