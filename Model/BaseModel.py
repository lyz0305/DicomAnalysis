

class BaseModel:

    def __init__(self):

        self.Observes = []

    def AddObserves(self, observe):

        self.Observes.append(observe)

    def Notify(self):

        for i in range(len(self.Observes)):

            self.Observes[i].Update(self.Name)

