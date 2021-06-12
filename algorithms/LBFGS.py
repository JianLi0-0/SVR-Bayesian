# -*- coding: utf-8 -*-
import numpy as np
import scipy.optimize as opt
from metrics import SimilarityMetrics as metrics
import ExtractSliceFromVolume as extractor
 
class LBFGS:
    
    name = "L-BFGS"
    success = False
    message = "no comments"
    niterations = 0
    
    def __init__(self, volume, sliceWidth, sliceHeight, outputSpacing, origin=(0,0,0)):
        self.__volume = volume
        self.__sliceWidth = sliceWidth
        self.__sliceHeight = sliceHeight
        self.__outputSpacing = outputSpacing
        self.__origin = origin
    
    def rosen(self, parameters):
        self.__transformation.SetParameters(parameters)
        slice = extractor.Execute(self.__volume, self.__transformation, self.__sliceWidth, self.__sliceHeight, self.__outputSpacing, self.__origin)
        return metrics.SumeOfSquareDifferences(slice, self.__goalSlice)
    
    def Execute(self, initialTransformation, goalSlice):
        self.__goalSlice = goalSlice
        self.__transformation = initialTransformation
        gradient = opt.approx_fprime(initialTransformation.GetParameters(), self.rosen, np.array([0.01, 0.01, 0.01, 1, 1, 1]))        
        res = opt.fmin_l_bfgs_b(self.rosen, initialTransformation.GetParameters(), fprime=gradient, approx_grad=1)
        self.success = True
        self.message = res[2]["task"]
        self.niterations = res[2]["nit"] 
        return res[0]

