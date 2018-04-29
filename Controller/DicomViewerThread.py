from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Controller import Log
from Model import DicomViewerModel
import SimpleITK as sitk
from Controller.TagName import Tags
class DicomHeaderReaderThread(QThread):

    @Log.LogClassFuncInfos
    def __init__(self):
        super(DicomHeaderReaderThread, self).__init__()
        self.__imageNames = None
        self.__sequenceInfoModel = DicomViewerModel.SequenceInfoModel()

    @Log.LogClassFuncInfos
    def setImageNames(self, names):
        self.__imageNames = names

    @Log.LogClassFuncInfos
    def setModel(self, model):
        if model.Name is self.SequenceInfoModel.Name:
            self.__sequenceInfoModel = model

    @Log.LogClassFuncInfos
    def run(self):
        reader = sitk.ImageFileReader()
        for dcmName in self.__imageNames:
            reader.SetFileName(dcmName)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            series_description = reader.GetMetaData(Tags['SeriesDescription'])
            series_number = reader.GetMetaData(Tags['SeriesNumber'])
            instance_number = reader.GetMetaData(Tags['InstanceNumber'])
            patient_name = reader.GetMetaData(Tags['PatientName'])
            name = series_number + ' ' + series_description
            SequenceInfo = self.SequenceInfoModel.GetSequenceInfo()
            if patient_name not in SequenceInfo.keys():
                SequenceInfo[patient_name] = dict()
            if name not in SequenceInfo[patient_name].keys():
                SequenceInfo[patient_name][name] = dict()
            SequenceInfo[patient_name][name][int(instance_number)] = dcmName
            # self.__sequenceInfoModel.SetSequenceInfo(SequenceInfo)
