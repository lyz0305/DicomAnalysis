

import SimpleITK as sitk

import pydicom as dicom
import numpy as np
import time

name = "G:\\SNAP_Signal_Analysis\\snap_simulation\\SNAP_TOF_Data\\Chang Cheng\\TOF\\IM_0180"
# pydicom
# T = time.localtime(time.time())
# print(T)
# for i in range(800):
#     Tag = ['PatientID','ImageType']
#     # ds = dicom.read_file("G:\\SNAP_Signal_Analysis\\snap_simulation\\SNAP_TOF_Data\\Chang Cheng\\TOF\\IM_0180",stop_before_pixels=True)
#     dicom.dcmread(name,specific_tags=Tag)
#     # image = np.array(ds.pixel_array)
#     # dicom.read_dicomdir()
# T = time.localtime(time.time())
# print(T)


# simple itk

T = time.localtime(time.time())
print(T)
reader = sitk.ImageFileReader()
for i in range(800):
    reader.SetFileName(name)
    reader.LoadPrivateTagsOn()
    reader.ReadImageInformation()
    keys = reader.GetMetaDataKeys()

T = time.localtime(time.time())
print(T)

import nibabel
