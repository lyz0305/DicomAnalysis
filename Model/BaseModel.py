
from Controller import Log
class BaseModel:

    @Log.LogClassFuncInfos
    def __init__(self):

        self.Observes = []

    @Log.LogClassFuncInfos
    def AddObserves(self, observe):
        N = len(self.Observes)
        for i in range(N):
            if observe.Name is self.Observes[i].Name:
                self.Observes[i] = observe
                return
        self.Observes.append(observe)

    @Log.LogClassFuncInfos
    def Notify(self):
        for i in range(len(self.Observes)):
            self.Observes[i].Update(self)

