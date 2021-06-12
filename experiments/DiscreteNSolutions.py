# -*- coding: utf-8 -*-
import numpy as np
import itertools
import Config
import ExtractSliceFromVolume
from datasets.HeartDataSet import HeartDataSet
from metrics import SimilarityMetrics
from libfastpd import fastpd

def make_pairs(nVars):
    listvars = np.arange(nVars)
    pairs = list(itertools.combinations(listvars, 2))
    return np.array(pairs, dtype=np.int32)
    
def getBinaries(transformation, volume, goalSlice, pairs):
    parameters = transformation.GetParameters()
    global labelings
    binaries = []
    for npair in range(len(pairs)):
        pair = pairs[npair]
        var1labels =  labelings[pair[0]]
        var2labels =  labelings[pair[1]]
        b = np.ones((len(var1labels), len(var2labels)), dtype=np.float32)
        for labelv1 in range(len(var1labels)):
            for labelv2 in range(len(var2labels)):   
                newTransformation = list(parameters)
                newTransformation[pair[0]] = var1labels[labelv1]
                newTransformation[pair[1]] = var2labels[labelv2]
                transformation.SetParameters(newTransformation)
                slice = ExtractSliceFromVolume.Execute(volume, transformation, goalSlice.GetWidth(), goalSlice.GetHeight(), list(goalSlice.GetSpacing()) + [1], (0,0,0))
                b[labelv1, labelv2] = SimilarityMetrics.SumeOfSquareDifferences(goalSlice, slice)
        binaries.append(b)
    return binaries    
    
def estimateLabelingTransformation(transformation, volume, goalSlice, nAlgorithmIter):
    nVars = len(transformation.GetParameters())
    pairs = make_pairs(nVars)
    u = np.ones((len(labelings[0]), nVars), dtype=np.float32)
    b = getBinaries(transformation, volume, goalSlice, pairs) 
    labeling = fastpd(u, b, pairs, nAlgorithmIter)  
    print "estimated labeling: " + str(labeling)
    estimatedTransformation = list(transformation.GetParameters())
    for nVar in range(len(labeling)):
        estimatedTransformation[nVar] = labelings[nVar][labeling[nVar]]
    return estimatedTransformation

def runDiscreteSolution(volume, transformation, goalSlice, nAlgorithmIter):
    estimatedTransformation = estimateLabelingTransformation(transformation, volume, goalSlice, nAlgorithmIter)
    transformation.SetParameters(estimatedTransformation)
    return transformation

def LoadTransformations(experimentName, method):
    data = {    
            'solutions': 0,
            'similarities': 0
            }
    path = Config.NSOLUTION_PATH + "/" + experimentName + "/" + Config.NSOLUTION_RESULTS_FILENAME
    transformations = []    
    similarities = []     
    with open(path) as file:
        for line in file:
            if line.startswith(method):
                line = file.next()
                line = line.replace("(", "")
                line = line.replace(")", "")
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace("\n", "")
                line = line.split(",")
                for i in range(len(line)):
                    line[i] = float(line[i].replace("'",""))
                transformations.append(line) 
                line = file.next()
                line = line.replace("\n", "")
                line = line.replace("'","")
                similarities.append(float(line))
    data['solutions'] = transformations
    data['similarities'] = similarities
    return data
    
def GetBestSolution(data):
    minimum = min(data['similarities'])
    print "minimum: " + str(minimum)
    indexM = data['similarities'].index(minimum)
    print "sol nº " + str(indexM) + "\n"
    return data['solutions'][indexM]
    
def GetLabelings(solutions):
    labelings = [[0 for i in range(len(solutions))] for j in range(len(solutions[0]))]
    for var in range(len(solutions[0])):
        for sol in range(len(solutions)):
            labelings[var][sol] = solutions[sol][var]
    return labelings
    
np.set_printoptions(precision=7)
np.set_printoptions(suppress=True)

experimentName = "LEJOS"
method = Config.DISCRETE
method = Config.CONTINUOUS

data = LoadTransformations(experimentName, method)
solutions = data['solutions']
similarities = data['similarities']
bestSolution = GetBestSolution(data)
print "best solution: " + str(bestSolution) + "\n"
print "similarities: " + str(similarities) + "\n"
print "solutions: " + str(solutions) + "\n"

labelings = GetLabelings(solutions)

image = 0
serie = 0
dataSet = HeartDataSet()
volume = dataSet.getVolume()
goalSlice = dataSet.getGoalSlice(serie,image)

nAlgorithmIter = 100
transformation = dataSet.getInitialTransformation(0)
transformation.SetParameters(bestSolution) 

estimatedSolution = runDiscreteSolution(volume, transformation, goalSlice, nAlgorithmIter)
#estimatedSolution.SetParameters([0.09999996461696155, 0.0000000387528727511549, 0.10000001017000898, 29.999999911050434,30.000003390632063, 15.000006176800682])

slice = ExtractSliceFromVolume.Execute(volume, estimatedSolution, goalSlice.GetWidth(), goalSlice.GetHeight(), list(goalSlice.GetSpacing()) + [1], (0,0,0))
SSD = SimilarityMetrics.SumeOfSquareDifferences(goalSlice, slice)
                
print "estimated solution: " + str(estimatedSolution.GetParameters())
print "estimated SSD: " + str(SSD)



