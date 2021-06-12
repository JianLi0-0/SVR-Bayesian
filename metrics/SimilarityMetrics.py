import SimpleITK as sitk
import numpy as np

def SumeOfAbsoluteDifferences(img1, img2):
    diff = 0
    for x in range(0,img1.GetWidth()):
        for y in range(0,img1.GetHeight()):
            diff = diff + abs(img1[x,y] - img2[x,y])
    return diff

def SumeOfSquareDifferences(img1, img2):
    # return SumeOfSquareDifferencesNormal(img1,img2)
    return SumeOfSquareDifferencesOptimize(img1,img2)
    
def SumeOfSquareDifferencesNormal(img1, img2):
    diff = 0
    for x in range(0,img1.GetWidth()):
        for y in range(0,img1.GetHeight()):
            diff = diff + (img1[x,y] - img2[x,y]) ** 2
    return diff
    
def SumeOfSquareDifferencesOptimize(img1, img2):
    
    input_image = sitk.GetArrayFromImage(img1)
    template  = sitk.GetArrayFromImage(img2)
    
    valid_mask = np.ones_like(template)
    total_weight = valid_mask.sum()
    window_size = template.shape
    ssd = np.empty((input_image.shape[0] - window_size[0] + 1,
                    input_image.shape[1] - window_size[1] + 1))
    for i in range(ssd.shape[0]):  
        for j in range(ssd.shape[1]):  
            sample = input_image[i:i + window_size[0], j:j + window_size[1]]  
            dist = (template - sample) ** 2  
            ssd[i, j] = (dist * valid_mask).sum()
    return ssd[0][0]
