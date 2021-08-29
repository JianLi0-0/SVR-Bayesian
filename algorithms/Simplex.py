# -*- coding: utf-8 -*-
import scipy.optimize as opt
from metrics import SimilarityMetrics as metrics
import ExtractSliceFromVolume as extractor

class Simplex:
    
    name = "simplex"
    success = False
    message = "not run"
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
    
    def Execute(self, initialTransformation, goalSlice, display):
        self.__goalSlice = goalSlice
        self.__transformation = initialTransformation
        res = opt.minimize(self.rosen, initialTransformation.GetParameters(), method='nelder-mead', options={'xtol': 1e-9, 'disp': display})
        self.success = res.success        
        self.message = res.message
        self.niterations = res.nit         
        return res.x