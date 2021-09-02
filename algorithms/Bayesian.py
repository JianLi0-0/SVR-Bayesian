# -*- coding: utf-8 -*-
import scipy.optimize as opt
from metrics import SimilarityMetrics as metrics
import ExtractSliceFromVolume as extractor
from bayes_opt import BayesianOptimization

class Bayesian:
    
    name = "Bayesian"
    success = False
    message = "not run"
    niterations = 0
    
    def __init__(self, volume, sliceWidth, sliceHeight, outputSpacing, origin=(0,0,0)):
        self.__volume = volume
        self.__sliceWidth = sliceWidth
        self.__sliceHeight = sliceHeight
        self.__outputSpacing = outputSpacing
        self.__origin = origin
    
    def rosen(self, rx, ry, rz, tx, ty, tz):
        a = self.__transformation.GetParameters()
        self.__transformation.SetParameters((rx, ry, rz, tx, ty, tz))
        slice = extractor.Execute(self.__volume, self.__transformation, self.__sliceWidth, self.__sliceHeight, self.__outputSpacing, self.__origin)
        return -metrics.SumeOfSquareDifferences(slice, self.__goalSlice)
    
    def Execute(self, initialTransformation, goalSlice, opt):
        self.__goalSlice = goalSlice
        self.__transformation = initialTransformation
        a = self.__transformation.GetParameters()
        # res = opt.minimize(self.rosen, initialTransformation.GetParameters(), method='nelder-mead', options={'xtol': 1e-9, 'disp': display})

        pbounds ={'rx': (-0.01, 0.3),
                  'ry': (1.45, 1.65),
                  'rz': (-0.06, 0.06),
                  'tx': (15, 40),
                  'ty': (7, 9.5),
                  'tz': (35, 55)}

        optimizer = BayesianOptimization(
            f=self.rosen,
            pbounds=pbounds,
            verbose=opt[2],
            random_state=1,
        )
        optimizer.maximize(
            init_points=opt[0],
            n_iter=opt[1],
        )
        return optimizer.max