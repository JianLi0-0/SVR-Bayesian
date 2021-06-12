import SimpleITK as sitk
from transformations import Rigid3D

def Generate(parameters, origin=(0,0,0)):
    rigid3D = Rigid3D.Generate(parameters, origin)
    transformation = sitk.ScaleVersor3DTransform()
    transformation.SetCenter(origin)    
    #transformation.SetParameters([x / 2.0 for x in parameters[0:3] ] + parameters[3:9])        
    transformation.SetTranslation(rigid3D.GetTranslation())
    transformation.SetScale(parameters[6:9])
    #transformation.SetRotation( [x / 2.0 for x in parameters[0:3] ])
    #print "ANI parameters: " + str(transformation.GetParameters())
    transformation.SetRotation( [x / 1.0 for x in parameters[0:3] ] + [1])
    print "ANI versor: " + str(transformation.GetVersor())
    return transformation