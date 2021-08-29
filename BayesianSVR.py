import ExtractSliceFromVolume
from metrics import SimilarityMetrics
from experiments import Optimization
import numpy as np
import time
from random import random
import SimpleITK as sitk
import matplotlib.pyplot as plt

from ultrasound_robot.srv import bayesian_svr, bayesian_svrResponse
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Image as ROS_IMAGE
import rospy
from cv_bridge import CvBridge

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import struct
import redis
import numpy as np


volume = sitk.ReadImage("/home/kuka/lee_ws/src/ultrasound_robot/src/python/new_biopsy_single_scaled.mha")

# slice_width = 256
# slcie_height = 256
spacing = volume.GetSpacing()[0]

# spacing = rospy.get_param("/svr/spacing") * rospy.get_param("/svr/volume_resol_reduction")
out_spacing = list((spacing, spacing)) + [1]
origin = (0,0,0)
# gt = (0.11,0.03,0.03, 10.0, 1.0, 35.0)
# groundtruth = sitk.Euler3DTransform()
# groundtruth.SetParameters(gt)
# goalSlice = ExtractSliceFromVolume.Execute(volume, groundtruth, slice_width, slcie_height, out_spaceing, origin)

bridge = CvBridge()
r = redis.Redis(host='localhost', port=6379, db=0)
def fromRedis(r,n):
    """Retrieve Numpy array from Redis key 'n'"""
    encoded = r.get(n)
    h, w = struct.unpack('>II',encoded[:8])
    a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w)
    return a

class BayesianSVR:
    def __init__(self):

        # rospy.Subscriber("/us_image", ROS_IMAGE, self.us_image_callback)
        self.servo_size = [rospy.get_param("/svr/servo_h"), rospy.get_param("/svr/servo_w")] 
        self.bayesian_svr_server()
    
    def us_image_callback(self, msg):
        self.ros_img = msg

    def Registration(self, req):
        self.cv2_img = fromRedis(r,'image')
        self.goalSlice = sitk.GetImageFromArray(self.cv2_img)
        self.goalSlice.SetSpacing((spacing, spacing))
        # print(self.goalSlice)
        t0 = time.time()
        angle_positon = Float64MultiArray()
        transformation = sitk.Euler3DTransform()
        solution = Optimization.BayesianRun(volume, self.goalSlice, origin, transformation, opt=(100, 300, 1))
        sol = [solution['params']['rx'], solution['params']['ry'], solution['params']['rz'], solution['params']['tx'], solution['params']['ty'], solution['params']['tz']]
        transformation.SetParameters(sol)
        solution = Optimization.SimplexRun(volume, self.goalSlice, origin, transformation, display=True) 
        self.finalSlice = ExtractSliceFromVolume.Execute(volume, solution, self.servo_size[1], self.servo_size[0], out_spacing, origin)
        angle_positon.data = solution.GetParameters()
        print("time cost", time.time() - t0)

        self.plot = True

        return bayesian_svrResponse(angle_positon, True)

    def bayesian_svr_server(self):
        self.s = rospy.Service('bayesian_svr', bayesian_svr, self.Registration)
        print("Ready to do the ultrasound image Registration.")
        rate = rospy.Rate(1)
        self.plot = False
        while rospy.is_shutdown() is False:
            if self.plot is True:
                fig = plt.figure(figsize=(10,5))
                ax = fig.add_subplot(1, 2, 1)
                plt.imshow(sitk.GetArrayFromImage(self.goalSlice), cmap=plt.cm.Greys_r)
                ax.set_title('goalSlice')
                ax = fig.add_subplot(1, 2, 2)
                plt.imshow(sitk.GetArrayFromImage(self.finalSlice), cmap=plt.cm.Greys_r)
                ax.set_title('finalSlice')
                plt.show()
                self.plot = False
            rate.sleep()
        rospy.spin()

if __name__ == "__main__":
    rospy.init_node('bayesian_svr_server')
    bayesian_svr = BayesianSVR()