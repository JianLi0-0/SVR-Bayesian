import os
from HeartDataSet import HeartDataSet
import ExtractSliceFromVolume
import SimilarityMetrics
import Config

dataSet = HeartDataSet()

maxRotationAngle = 0.01#0.01
maxTranslation = 5#5
modificationRate = 0.03#0.03
nSteps = 5 # number of labels
nIters = 600
nAlgorithmIter = 100
image = 0
serie = 0

modificationRates = [0.03, 0.05, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

directory = Config.ANALISIS_PATH + "/ModificationRate"
if not os.path.exists(directory):
    os.makedirs(directory)
with open(directory + "/results_1st_image_all_series.txt",'a+') as file:
    file.write("MODIFICATION RATE CROSS-VALIDATION:\n\n")        
    file.write("EXPERIMENT PARAMETERS:\n")        
    file.write("Max rotation angle:         " + str(maxRotationAngle) + "\n")    
    file.write("Max translation:            " + str(nSteps) + "\n")    
    file.write("Number of labels:           " + str(nSteps) + "\n")    
    for rate in range(len(modificationRates)):
        modificationRate = modificationRates[rate]
        file.write("\nModification rate: " + str(modificationRate) + "\n") 
        for serie in range(9):  
            initialTransformation = dataSet.getInitialTransformation(serie+1)
            solution = runDiscreteSolution(initialTransformation, dataSet.getGoalSlice(serie+1, image), maxRotationAngle, maxTranslation, nSteps, modificationRate, nAlgorithmIter, nIters)
            slice = ExtractSliceFromVolume.Execute(dataSet, solution)
            file.write(str(SimilarityMetrics.SumeOfSquareDifferences(dataSet.getGoalSlice(serie+1, image) , slice)) + ", ")
        file.write("\n")

"""        
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 HASTA NO HACER ANDAR LOS LLAMADOS AL .py QUE TIENE LA PARALELIZACION, ESTO NO ANDA. COPIAR ALLÍ
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""