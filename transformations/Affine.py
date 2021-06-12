import random
import SimpleITK as sitk

def Generate(parameters, origin=(0,0,0)):
    transformation = sitk.AffineTransform(len(origin))
    transformation.SetCenter(origin)
    transformation.SetTranslation(parameters[9:12])
    transformation.SetMatrix(parameters[0:9])
    return transformation
    
def GenerateRandom(initial, maxM, maxTr):
    parameters = []    
    for i in range(len(initial)):
        if i < 9:
            parameters.append(initial[i] + random.uniform(-maxM, maxM))
        else:            
            parameters.append(initial[i] + random.uniform(-maxTr, maxTr))
    return Generate(parameters)