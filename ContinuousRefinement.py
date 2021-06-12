import Config
import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from experiments import PyramidSimplex, PyramidOthers, Optimization
from datasets.HeartDataSet import HeartDataSet
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt

dataSet = HeartDataSet()

nserie = 0
nslice = 3

gt = (0.15, 0.0, 0.05, 25.0, 25.0, 15.0)
groundtruth = sitk.Euler3DTransform()
groundtruth.SetParameters(gt)

random_ratio = 0.1
init_tf = tuple(map(lambda x: (1+random_ratio*2*(0.5-random()))*x, groundtruth.GetParameters()))
transformation = sitk.Euler3DTransform()
transformation.SetParameters(init_tf)

volume = dataSet.getVolume() 
goalSlice = ExtractSliceFromVolume.Execute(dataSet.getVolume(), groundtruth, dataSet.getGoalSlice(nserie, nslice).GetWidth(), dataSet.getGoalSlice(nserie, nslice).GetHeight(), list(dataSet.getGoalSlice(nserie, nslice).GetSpacing()) + [1], dataSet.getOrigin())
origin = dataSet.getOrigin()

# print(goalSlice)

print("initial tf:" + str(transformation.GetParameters()))
print("groundtruth:" + str(groundtruth.GetParameters()))

t0 = time.time()
solution = Optimization.SimplexRun(volume, goalSlice, origin, transformation, display=True)
print("solution:" + str(solution.GetParameters()))
print(str(np.array(groundtruth.GetParameters())-np.array(solution.GetParameters())))
print(time.time() - t0)