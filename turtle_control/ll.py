#!/usr/bin/env python3
import math
import string
import numpy as np
import rospy
import roslaunch
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool,Float32,Int32MultiArray,String
from turtlesim.msg import Pose as tPose
from std_srvs.srv import Empty, EmptyResponse
import rospy
import os
import rospy
import subprocess
import roslaunch
from std_srvs.srv import Trigger, TriggerResponse

n=0


def test():
        package = 'turtle_control'
        launch_file = 'case2.launch'

        command = "roslaunch  {0} {1}".format(package, launch_file)

        p = subprocess.Popen(command, shell=True)

        state = p.poll()
 

if __name__ == '__main__':
    rospy.init_node('test1', anonymous=True)
    test()
    # service = rospy.Service('launch', Trigger, service_callback)

    rospy.spin()


































# class Node:
#     def __init__(self):
#         self.timer = None
#         self.n=0
#         self.pos=[]
#         self.collect=[]
#         self.get=0
#         self.pre_vp=[]
#     def callback_viapoint(self,msg):
#         self.collect = msg.data

#     def call_viapoint(self,msg):
#         rospy.Subscriber('/idle_viapoint',Int32MultiArray,node.callback_viapoint)
#         if len(self.collect)==2 and self.pre_vp!=self.collect:
#             self.pre_vp=self.collect
#             # rospy.loginfo(self.collect)
#             self.collect_via()
#         # self.collect = msg.data
#         # while not rospy.is_shutdown():

 
#     def collect_via(self):
#         if len(self.collect)!=0 and self.get==0:
#             self.pos.append(self.collect)
#             rospy.loginfo(self.pos)
#             # pub something
#             canrun = str()
#             canrun = 'donesent' 
#             pub.publish(canrun)
#             # self.get=1

#     def callback_shutDownTimer(self):
#         self.timer.shutdown()

# if __name__ == '__main__':
#     rospy.loginfo("started")
#     rospy.init_node('ll')
#     node =Node()
#     pub = rospy.Publisher('senddone',String,queue_size=10)
#     timer = rospy.Timer(rospy.Duration(1/10), node.call_viapoint)
#     rospy.spin()

