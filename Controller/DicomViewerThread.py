from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Controller import Log
from Model import DicomViewerModel
import SimpleITK as sitk
from Controller.TagName import Tags
import time
class DicomHeaderReaderThread(QThread):

    # the aDicomFinish emit: patientName, seryName, instanceNumber, path
    aDicomFinish = pyqtSignal(str, str, int, str)
    allDicomFinish = pyqtSignal()

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomHeaderReaderThread, self).__init__()
        self.__imageNames = None
        self.__sequenceInfo = dict()


    @Log.LogClassFuncInfos
    def setImageNames(self, names):
        self.__imageNames = names

    @Log.LogClassFuncInfos
    def setSequenceInfo(self, sequenceInfo):
        self.__sequenceInfo = sequenceInfo

    @Log.LogClassFuncInfos
    def aDicomFinishConnect(self, func):
        self.aDicomFinish.connect(func)

    @Log.LogClassFuncInfos
    def allDicomFinishConnect(self, func):
        self.allDicomFinish.connect(func)

    @Log.LogClassFuncInfos
    def run(self):
        N = len(self.__imageNames)
        reader = sitk.ImageFileReader()

        # while 1:
        #     print('run')
        #     self.msleep(10)
        for i in range(N):
            dcmName = self.__imageNames[i]
            reader.SetFileName(dcmName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            series_description = reader.GetMetaData(Tags['SeriesDescription'])
            series_number = reader.GetMetaData(Tags['SeriesNumber'])
            instance_number = reader.GetMetaData(Tags['InstanceNumber'])
            patient_name = reader.GetMetaData(Tags['PatientName'])
            name = series_number + ' ' + series_description

            if patient_name not in self.__sequenceInfo.keys():
                self.__sequenceInfo[patient_name] = dict()
            if name not in self.__sequenceInfo[patient_name].keys():
                self.__sequenceInfo[patient_name][name] = dict()
            self.__sequenceInfo[patient_name][name][int(instance_number)] = dcmName
            self.aDicomFinish.emit(patient_name, name, int(instance_number), dcmName)
            # self.msleep(50)
        self.allDicomFinish.emit()
