
import time
import os


IsLogTrace = True


logname = 'DicomTool.log'
def LogTrace(name):
    if IsLogTrace == False:
        return

    T = time.localtime(time.time())
    with open(logname,'a+') as f:
        f.write('%s,%04d%02d%02d%02d%02d%02d\n'%(name, T.tm_year, T.tm_mon, T.tm_mday,
                                               T.tm_hour, T.tm_min, T.tm_sec))

def removeLog():

    os.remove(logname)

if __name__ == '__main__':

    LogTrace('test')
    LogTrace('test2')