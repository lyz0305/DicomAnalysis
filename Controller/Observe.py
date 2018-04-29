
import Controller.Log as Log
import sys

class Observe:

    @Log.LogClassFuncInfos
    def __init__(self):
        pass

    @Log.LogClassFuncInfos
    def update(self,model):
        sys.exit('Controller must rewrite the Update function')
