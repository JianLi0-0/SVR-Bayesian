# -*- coding: utf-8 -*-
import scipy.optimize as opt
from metrics import SimilarityMetrics as metrics
import ExtractSliceFromVolume as extractor

import numpy as np
 
class BFGS:
    
    name = "BFGS"
    success = True
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
    
    def fprime(self, initialTransformation):
        return opt.approx_fprime(initialTransformation, self.rosen, np.array([0.01, 0.01, 0.01, 1, 1, 1]))  
    
    def Execute(self, initialTransformation, goalSlice):
        self.__goalSlice = goalSlice
        self.__transformation = initialTransformation
        #res = opt.fmin_bfgs(self.rosen, initialTransformation, fprime=self.fprime )
        #res = opt.fmin_bfgs(self.rosen, initialTransformation, fprime=None, epsilon=np.array([0.01, 0.01, 0.01, 1, 1, 1]))  
        res = opt.fmin_bfgs(self.rosen, initialTransformation.GetParameters(), fprime=None)
        
        """self.success = res.success        
        self.message = res.message
        self.niterations = res.nit"""         
        return res
