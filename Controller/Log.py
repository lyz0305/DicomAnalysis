
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

            if len(s) == 1:
                f.write('%s, %04d%02d%02d%02d%02d%02d\n' % (methodName, T.tm_year, T.tm_mon, T.tm_mday,
                                                           T.tm_hour, T.tm_min, T.tm_sec))
            elif len(s) >= 2:
                className = format(self.__class__.__name__)
                f.write('%s, %s, %04d%02d%02d%02d%02d%02d\n' % (className, methodName, T.tm_year, T.tm_mon, T.tm_mday,
                                                            T.tm_hour, T.tm_min, T.tm_sec))

        numberOfSpace = numberOfSpace + 1
        ret = func(*s, **gs)
        numberOfSpace = numberOfSpace - 1
        return ret

    return wrapper

if __name__ == '__main__':

    LogTrace('test')
    LogTrace('test2')