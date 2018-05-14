


BTNNormal = 0 # pan, zoom contrast

BTNFreeHandROIDraw = 1 # free hand roi draw
BTNFreeHandROIErase = 2

BTNStatus = 0 # pan, zoom contrast

def getBTNStatus():
    return BTNStatus

def setBTNToFreeHandROIDraw():
    global BTNStatus
    BTNStatus = BTNFreeHandROIDraw

def setBTNToFreeHandROIErase():
    global BTNStatus
    BTNStatus = BTNFreeHandROIErase

def setBTNToNormal():
    global BTNStatus
    BTNStatus = BTNNormal

if __name__ == '__main__':

    a = getBTNStatus()
    print(a)
    setBTNToFreeHandROIDraw()
    print(getBTNStatus())