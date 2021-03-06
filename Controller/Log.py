
import time
import os
import sys

IsLogTrace = True

global numberOfSpace
numberOfSpace = 0
logname = 'DicomTool.log'

def removeLog():
    if os.path.exists(logname):
        os.remove(logname)

def LogClassFuncInfos(func):

    def wrapper(*s, **gs):
        T = time.localtime(time.time())
        self = s[0]
        methodName = format(func.__name__)
        global numberOfSpace
        with open(logname, 'a+') as f:
            for i in range(numberOfSpace):
                f.write('\t')

            className = format(self.__class__.__name__)
            f.write('%04d%02d%02d%02d%02d%02d, %s, %s\n' % (T.tm_year, T.tm_mon, T.tm_mday,
                                                            T.tm_hour, T.tm_min, T.tm_sec,
                                                            className, methodName))

        numberOfSpace = numberOfSpace + 1
        ret = func(*s, **gs)
        numberOfSpace = numberOfSpace - 1
        return ret

    return wrapper

if __name__ == '__main__':

    LogTrace('test')
    LogTrace('test2')