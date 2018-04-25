
import Controller.Log as Log
import sys

class Observe:

    def __init__(self):

        Log.LogTrace('Observe, Init')

    def Update(self,model):
        Log.LogTrace('Observe, model')
        sys.exit('Controller must rewrite the Update function')
