import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from experiments import Optimization
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt

volume = sitk.ReadImage("./dataset_basico/volumen/thyroid.mhd")

slice_width = 256
slcie_height = 256
spacing = volume.GetSpacing()[0]
out_spaceing = list((spacing, spacing)) + [1]
origin = (0,0,0)

gt = (0.1, 0.1, 0.1, 5.0, 5.0, spacing*464*0.5)
groundtruth = sitk.Euler3DTransform()
groundtruth.SetParameters(gt)

random_ratio = 0.1
init_tf = tuple(map(lambda x: (1+random_ratio*2*(0.5-random()))*x, groundtruth.GetParameters()))
transformation = sitk.Euler3DTransform()
transformation.SetParameters(init_tf)


goalSlice = ExtractSliceFromVolume.Execute(volume, groundtruth, slice_width, slcie_height, out_spaceing, origin)
initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
# print(goalSlice)

print("initial tf:" + str(transformation.GetParameters()))
print("groundtruth:" + str(groundtruth.GetParameters()))

t0 = time.time()
solution = Optimization.SimplexRun(volume, goalSlice, origin, transformation, display=True)
print("solution:" + str(solution.GetParameters()))
print(str(np.array(groundtruth.GetParameters())-np.array(solution.GetParameters())))
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