import SimpleITK as sitk
import time
# Extract slice from a volume with a given transformation

def Execute(volume, transformation, sliceWidth, sliceHeight, outputSpacing, origin=(0,0,0)):
    # t0 = time.time()
    filter = sitk.ResampleImageFilter()
    filter.SetSize((sliceWidth,sliceHeight,1))
    filter.SetOutputOrigin(origin)
    filter.SetOutputSpacing(outputSpacing)
    filter.SetOutputDirection((1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0))
    filter.SetTransform(transformation)
    
    output3DSlice = filter.Execute(volume)
    
    # print("interval: " + str(time.time()-t0))
    # t0 = time.time()

    zindex = 0 # in order to get the first slice (in this case, the onlyone) in z axis 
    Extractor = sitk.ExtractImageFilter()
    Extractor.SetSize( [ sliceWidth, sliceHeight, 0 ] )
    Extractor.SetIndex( [ 0, 0, zindex ] )
    
    output2DSlice = Extractor.Execute(output3DSlice)
    # print("interval: " + str(time.time()-t0))
    return output2DSlice

def Execute2(volume, transformation, sliceWidth, sliceHeight, outputSpacing, origin=(0,0,0)):
    t0 = time.time()
    filter = sitk.ResampleImageFilter()
    filter.SetSize((sliceWidth,sliceHeight,0))
    filter.SetOutputOrigin(origin)
    filter.SetOutputSpacing(outputSpacing)
    filter.SetOutputDirection((1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0))
    filter.SetTransform(transformation)
    
    output2DSlice = filter.Execute(volume)
    
    print("interval: " + str(time.time()-t0))
    # t0 = time.time()

    # zindex = 0 # in order to get the first slice (in this case, the onlyone) in z axis 
    # Extractor = sitk.ExtractImageFilter()
    # Extractor.SetSize( [ sliceWidth, sliceHeight, 0 ] )
    # Extractor.SetIndex( [ 0, 0, zindex ] )
    
    # output2DSlice = Extractor.Execute(output3DSlice)
    # print("interval: " + str(time.time()-t0))
    return output2DSlice

