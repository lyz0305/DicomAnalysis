
import Controller.Log as Log
import sys

class Observe:

    @Log.LogClassFuncInfos
    def __init__(self):
        pass

    @Log.LogClassFuncInfos
    def Update(self,model):
        sys.exit('Controller must rewrite the Update function')
