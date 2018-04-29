
from Controller import Log
class BaseModel:

    @Log.LogClassFuncInfos
    def __init__(self):

        self.__observes = []

    @Log.LogClassFuncInfos
    def AddObserves(self, observe):
        N = len(self.__observes)
        for i in range(N):
            if observe.Name is self.__observes[i].Name:
                self.__observes[i] = observe
                return
        self.__observes.append(observe)

    @Log.LogClassFuncInfos
    def Notify(self):
        for i in range(len(self.__observes)):
            self.__observes[i].update(self)

