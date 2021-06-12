import random
import SimpleITK as sitk

def Generate(parameters, origin=(0,0,0)):  
    transformation = sitk.Euler3DTransform()
    transformation.SetCenter(origin)
    transformation.SetParameters(parameters)
    return transformation
    
def GenerateRandom(initial, maxRot, maxTr):
    parameters = []    
    for i in range(len(initial)):
        if i < 3:
            parameters.append(initial[i] + random.uniform(-maxRot, maxRot))
        else:            
            parameters.append(initial[i] + random.uniform(-maxTr, maxTr))
    return Generate(parameters)
    
def GenerateRandomAway(initial, minRot, maxRot, minTr, maxTr):
    parameters = []    
    for i in range(len(initial)):
        if i < 3:
            parameters.append(initial[i] + random.uniform(minRot, maxRot) * random.choice([-1,1]))
        else:            
            parameters.append(initial[i] + random.uniform(minTr, maxTr) * random.choice([-1,1]))
    return Generate(parameters)