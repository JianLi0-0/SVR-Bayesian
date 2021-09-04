import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from metrics import SimilarityMetrics as metrics
from experiments import Optimization
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt
import math

volume = sitk.ReadImage("/home/kuka/SVR/Slice_to_Volume_Registration_Python/dataset/thyroid.mhd")

slice_width = 256
slcie_height = 256
spacing = volume.GetSpacing()[0]
out_spaceing = list((spacing, spacing)) + [1]
origin = (0,0,0)

gt = (0.11,0.03,0.03, 0.0, 0.0, 30.0)
groundtruth = sitk.Euler3DTransform()
groundtruth.SetParameters(gt)
goalSlice = ExtractSliceFromVolume.Execute(volume, groundtruth, slice_width, slcie_height, out_spaceing, origin)
transformation = sitk.Euler3DTransform()

x_list = []
ssd_list1 = []
ssd_list2 = []
ssd_list3 = []
points_num = 800
span = 20
for i in range(points_num+1):
    x_list.append((i/points_num-0.5)*span*2)
    init_tf = ( gt[0], gt[1], gt[2], gt[3]+(i/points_num-0.5)*span*2, gt[4], gt[5] )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list1.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

    init_tf = ( gt[0], gt[1], gt[2], gt[3], gt[4]+(i/points_num-0.5)*span*2, gt[5] )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list2.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

    init_tf = ( gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]+(i/points_num-0.5)*span*2 )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list3.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

np.savetxt("position.txt",np.array([x_list, ssd_list1, ssd_list2, ssd_list3]).transpose(1,0))     #将数组中数据写入到data.txt文件
# plt.plot(x_list, ssd_list1)
# plt.plot(x_list, ssd_list2)
# plt.plot(x_list, ssd_list3)
# plt.show()

x_list = []
ssd_list1 = []
ssd_list2 = []
ssd_list3 = []
points_num = 800
span = math.pi/3
for i in range(points_num):
    x_list.append((i/points_num-0.5)*span*2)
    init_tf = ( gt[0]+(i/points_num-0.5)*span*2, gt[1], gt[2], gt[3], gt[4], gt[5] )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list1.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

    init_tf = ( gt[0], gt[1]+(i/points_num-0.5)*span*2, gt[2], gt[3], gt[4], gt[5] )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list2.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

    init_tf = ( gt[0], gt[1], gt[2]+(i/points_num-0.5)*span*2, gt[3], gt[4], gt[5] )
    transformation.SetParameters(init_tf)
    initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
    ssd_list3.append(metrics.SumeOfSquareDifferences(initSlice, goalSlice))

np.savetxt("rotation.txt",np.array([x_list, ssd_list1, ssd_list2, ssd_list3]).transpose(1,0))  
# plt.plot(x_list, ssd_list1)
# plt.plot(x_list, ssd_list2)
# plt.plot(x_list, ssd_list3)
# plt.show()


# plt.imshow(sitk.GetArrayFromImage(goalSlice), cmap=plt.cm.Greys_r)
# plt.show()

# plt.plot(x_list, ssd_list1)
# plt.plot(x_list, ssd_list2)
# plt.plot(x_list, ssd_list3)
# plt.show()