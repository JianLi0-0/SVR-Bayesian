import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation
from pytransform3d.plot_utils import Frame
from pytransform3d import rotations as pr

n_frames = 25

################################################################
import Config
import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from experiments import PyramidSimplex, PyramidOthers, Optimization
from datasets.HeartDataSet import HeartDataSet
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

volume = sitk.ReadImage("./dataset_basico/volumen/thyroid.mhd")

nserie = 0
nslice = 3
slice_width = 256
slcie_height = 256
spacing = volume.GetSpacing()[0]
out_spaceing = list((spacing, spacing)) + [1]
origin = (0,0,0)


gt = (0.25, 0.25, 0.1, 5.0, 5.0, spacing*464*0.2)
groundtruth = sitk.Euler3DTransform()
groundtruth.SetParameters(gt)
# print("step:"+str(1/n_frames*spacing*464*0.5)) # 2.18

random_ratio = 0.05
init_tf = tuple(map(lambda x: (1+random_ratio*2*(0.5-random()))*x, groundtruth.GetParameters()))
transformation = sitk.Euler3DTransform()
transformation.SetParameters(init_tf)

def rand_one():
    return 2*(0.5-random())
pi = 3.1415926

# initSlice = ExtractSliceFromVolume.Execute(volume, transformation, slice_width, slcie_height, out_spaceing, origin)
cnt= 0
################################################################



base2current = np.eye(4)
base2registered = np.eye(4)

def update_frame(step, n_frames, current_frame, registered_frame):
    # angle = 2.0 * np.pi * (step + 1) / n_frames
    # print(step)
    # R = pr.matrix_from_angle(0, angle)
    # A2B = np.eye(4)
    # A2B[:3, :3] = R
    ################################################################
    global gt
    if gt[5] > spacing*464*0.85: 
        return current_frame, registered_frame
    motion = (2/180*pi*rand_one(),2/180*pi*rand_one(),2/180*pi*rand_one(),0*rand_one(),0*rand_one(),1/n_frames*spacing*464*0.5)
    gt = tuple(map(sum, zip(motion, gt)))
    groundtruth.SetParameters(gt)
    goalSlice = ExtractSliceFromVolume.Execute(volume, groundtruth, slice_width, slcie_height, out_spaceing, origin)
    solution = Optimization.SimplexRun(volume, goalSlice, origin, transformation, display=False)
    # print(R.from_euler('xyz', groundtruth.GetParameters()[0:3]))
    base2current[:3, :3] = R.from_euler('xyz', groundtruth.GetParameters()[0:3]).as_dcm()
    base2current[:3, -1] = groundtruth.GetParameters()[3:]
    base2current[:3, -1] = base2current[:3, -1]/1000.0
    base2registered[:3, :3] = R.from_euler('xyz', solution.GetParameters()[0:3]).as_dcm()
    base2registered[:3, -1] = solution.GetParameters()[3:]
    base2registered[:3, -1] = base2registered[:3, -1]/1000.0
    # print(base2current)
    # print(base2registered)
    # global cnt
    # cnt = cnt +1
    # writer = sitk.ImageFileWriter()
    # writer.SetFileName("./output/"+str(cnt)+".nii")
    # writer.Execute(goalSlice)
    print(str(np.array(groundtruth.GetParameters())-np.array(solution.GetParameters())))
    ################################################################
    
    current_frame.set_data(base2current)
    registered_frame.set_data(base2registered)
    return current_frame, registered_frame

T = np.eye(4)
T[2][3]=0.05

if __name__ == "__main__":
    

    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim((0, 0.02))
    ax.set_ylim((0, 0.02))
    ax.set_zlim((0, 0.15))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    current_frame = Frame(T, label="current_frame", s=0.005)
    current_frame.add_frame(ax)

    registered_frame = Frame(T, label="registered_frame", s=0.005)
    registered_frame.add_frame(ax)

    base_frame = Frame(np.eye(4), label="base frame", s=0.005)
    base_frame.add_frame(ax)

    anim = animation.FuncAnimation(
        fig, update_frame, n_frames, fargs=(n_frames, current_frame, registered_frame), interval=50,
        blit=False)

    plt.show()
