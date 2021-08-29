# -*- coding: utf-8 -*-
from algorithms.Simplex import Simplex
from algorithms.Powell import Powell
from algorithms.BFGS import BFGS
from algorithms.LBFGS import LBFGS
from algorithms.Bayesian import Bayesian

def SimplexRun(volume, goalSlice, origin, transformation, display):  
    sliceWidth = goalSlice.GetWidth()
    sliceHeight = goalSlice.GetHeight()
    # print("sliceWidth"+str(sliceWidth))
    # print("sliceHeight"+str(sliceHeight))
    outputSpacing = list(goalSlice.GetSpacing()) + [1]
    # print(outputSpacing)
    registration = Simplex(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
    solution = registration.Execute(transformation, goalSlice, display)
    transformation.SetParameters(solution)
    return transformation

def BayesianRun(volume, goalSlice, origin, transformation, opt): 
    sliceWidth = goalSlice.GetWidth()
    sliceHeight = goalSlice.GetHeight()
    outputSpacing = list(goalSlice.GetSpacing()) + [1]
    registration = Bayesian(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
    solution = registration.Execute(transformation, goalSlice, opt)
    return solution

def PowellRun(volume, goalSlice, origin, transformation):  
    sliceWidth = goalSlice.GetWidth()
    sliceHeight = goalSlice.GetHeight()
    outputSpacing = list(goalSlice.GetSpacing()) + [1]
    registration = Powell(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
    solution = registration.Execute(transformation, goalSlice)
    transformation.SetParameters(solution)
    return transformation

def BFGSRun(volume, goalSlice, origin, transformation):  
    sliceWidth = goalSlice.GetWidth()
    sliceHeight = goalSlice.GetHeight()
    outputSpacing = list(goalSlice.GetSpacing()) + [1]
    registration = BFGS(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
    solution = registration.Execute(transformation, goalSlice)
    transformation.SetParameters(solution)
    return transformation

def LBFGSRun(volume, goalSlice, origin, transformation):  
    sliceWidth = goalSlice.GetWidth()
    sliceHeight = goalSlice.GetHeight()
    outputSpacing = list(goalSlice.GetSpacing()) + [1]
    registration = LBFGS(volume, sliceWidth, sliceHeight, outputSpacing, origin)   
    solution = registration.Execute(transformation, goalSlice)
    transformation.SetParameters(solution)
    return transformation