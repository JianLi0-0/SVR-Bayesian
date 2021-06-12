import os
import numpy as np
import Config
import DiscreteOptimizedRegistration as discrete
from HeartDataSet import HeartDataSet

"""
directory = Config.ANALISIS_PATH + "/ModificationRate"

if not os.path.exists(directory):
    os.makedirs(directory)

with open(directory + "/results.txt",'w') as file:
    file.write("RESULTADOS EXPERIMENTOS:\n")
"""




# solution slice: 0.1  -0.    0.1  30.   30.   15.    
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
dataSet = HeartDataSet()
initialTransformation = dataSet.getInitialTransformation(0).copy()
maxRotationAngle = 0.01#0.01
maxTranslation = 5#5
modificationRate = 0.08#0.03
nSteps = 5 # number of labels
nIters = 1
nAlgorithmIter = 100

discrete.runDiscreteSolution(initialTransformation, maxRotationAngle, maxTranslation, nSteps, modificationRate, nAlgorithmIter, nIters)
