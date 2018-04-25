
from Controller.Log import *
class BaseModel:

    def __init__(self):

        self.Observes = []

    def AddObserves(self, observe):

        LogTrace('BaseModel, AddObserves, '+observe.Name)
        N = len(self.Observes)
        for i in range(N):
            if observe.Name is self.Observes[i].Name:
                self.Observes[i] = observe
                return
        self.Observes.append(observe)

    def Notify(self):

        for i in range(len(self.Observes)):

            self.Observes[i].Update(self)

