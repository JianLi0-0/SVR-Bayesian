# -*- coding: utf-8 -*-
# from Pyramid import Pyramid
from algorithms.Simplex import Simplex
import Config

def Run(dataSet, serie, image, transformation, numberOfLevels):
    volume = dataSet.getVolume()   
    goalSlice = dataSet.getGoalSlice(serie, image)
    pyramid3D = Pyramid(volume.GetDimension(),Config.CONTINUOUS)
    pyramid2D = Pyramid(goalSlice.GetDimension(),Config.CONTINUOUS)
    #pyramid3D.createPyramid(dataSet.getVolumePath(),numberOfLevels,1)
    pyramid2D.createPyramid(dataSet.getGoalSlicePath(serie, image),numberOfLevels)
    
    for level in range(numberOfLevels):
        volume = pyramid3D.getLevel(level)
        goalSlice = pyramid2D.getLevel(level)        
        sliceWidth = goalSlice.GetWidth()
        sliceHeight = goalSlice.GetHeight()
        outputSpacing = list(goalSlice.GetSpacing()) + [1]
        origin = dataSet.getOrigin()        
        registration = Simplex(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
        solution = registration.Execute(transformation, goalSlice)
        transformation.SetParameters(solution)
    return transformation