
import time
import sys

def LogClassFuncInfos(func):

    def wrapper(*s, **gs):
        methodName = format(func.__name__)
        print(methodName)
        print('start')
        ret = func(*s, **gs)
        print('end')
        return ret

    return wrapper

class NameModel():

    def __init__(self):
        self.name = 'test'

    @LogClassFuncInfos
    def getName(self):
        print('run function')
        return self.name

a = NameModel()
print(a.getName())

