import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from experiments import Optimization
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt

volume = sitk.ReadImage("/home/kuka/SVR/Slice_to_Volume_Registration_Python/dataset/thyroid.mhd")

slice_width = 256
slcie_height = 256
spacing = volume.GetSpacing()[0]
out_spaceing = list((spacing, spacing)) + [1]
origin = (0,0,0)

gt = (0.11,0.03,0.03, 10.0, 1.0, 35.0)
groundtruth = sitk.Euler3DTransform()
groundtruth.SetParameters(gt)

random_ratio = 0.1
# init_tf = tuple(map(lambda x: (1+random_ratio*2*(0.5-random()))*x, groundtruth.GetParameters()))
# init_tf = ( gt[0]-0.003, gt[1]-0.003, gt[2]-0.003, gt[3]+3, gt[4]+3, gt[5]+3 )
init_tf = (0, 0, 0, 0, 0, 0)
transformation = sitk.Euler3DTransform()
transformation.SetParameters(init_tf)


goalSlice = ExtractSliceFromVolume.Execute(volume, groundtruth, slice_width, slcie_height, out_spaceing, origin)
initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
# print(goalSlice)

print("initial tf:" + str(transformation.GetParameters()))
print("groundtruth:" + str(groundtruth.GetParameters()))

t0 = time.time()
solution = Optimization.BayesianRun(volume, goalSlice, origin, transformation, opt=(100, 300, 1)) # opt[init_points, n_iter, verbose]

print("solution:" + str(solution['params']))
print("ssd:" + str(-solution['target']))
# print(str(np.array(groundtruth.GetParameters())-np.array(solution.GetParameters())))
print(time.time() - t0)

sol = [gt[0], gt[1], gt[2], solution['params']['tx'], solution['params']['ty'], solution['params']['tz']]

transformation.SetParameters(sol)
solution = Optimization.SimplexRun(volume, goalSlice, origin, transformation, display=True) 
print("NM_solution:" + str(solution.GetParameters()))
print(time.time() - t0)

finalSlice = ExtractSliceFromVolume.Execute(volume, solution, slice_width, slcie_height, out_spaceing, origin)
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1, 3, 1)
plt.imshow(sitk.GetArrayFromImage(goalSlice), cmap=plt.cm.Greys_r)
ax.set_title('goalSlice')

ax = fig.add_subplot(1, 3, 2)
plt.imshow(sitk.GetArrayFromImage(finalSlice), cmap=plt.cm.Greys_r)
ax.set_title('finalSlice')

ax = fig.add_subplot(1, 3, 3)
plt.imshow(sitk.GetArrayFromImage(initSlice), cmap=plt.cm.Greys_r)
ax.set_title('initSlice')

plt.show()