import SimpleITK as sitk
import random
from transformations import Rigid3D

def Generate(parameters, origin=(0,0,0)):
    rigid3D = Rigid3D.Generate(parameters, origin)
    transformation = sitk.Similarity3DTransform()
    transformation.SetCenter(rigid3D.GetCenter())
    transformation.SetMatrix(rigid3D.GetMatrix())
    transformation.SetTranslation(rigid3D.GetTranslation())
    transformation.SetScale(parameters[6])
    return transformation
    
def GenerateRandom(initial, maxRot, maxTr, maxSc):
    parameters = []    
    for i in range(len(initial) - 1):
        if i < 3:
            parameters.append(initial[i] + random.uniform(-maxRot, maxRot))
        else:            
            parameters.append(initial[i] + random.uniform(-maxTr, maxTr))
    parameters.append(initial[6] + random.uniform(-maxSc, maxSc))
    return Generate(parameters)