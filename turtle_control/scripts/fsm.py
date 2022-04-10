#!/usr/bin/env python3
from ast import Str
import math
from multiprocessing import Condition
from sre_parse import State
import string
import numpy as np
import rospy
import roslaunch
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool,Float32,Int32MultiArray,String
from turtlesim.msg import Pose as tPose
from std_srvs.srv import Empty, EmptyResponse
import roslaunch


class Node :
    def __init__(self):
        self.timer = None
        self.turtle_state = 0
        self.current_position = np.array([5.5445,5.5445])
        self.n=0
        self.n2=0
        self.ispub3 = str()
        self.ispub2 = str()
        self.tstate =0
        self.tstate2 =0
        self.uuid2=0

    def callback_current_pose(self,msg):
        self.current_position  = np.array([msg.x,msg.y])

    def check_pub2(self,msg):
        self.ispub2 = msg.data
        if self.ispub2=='case2done':
            rospy.loginfo('True2')
        # self.ispub2=='case2done
    def check_pub3(self,msg):
        self.ispub3 = msg.data
        if self.ispub3=='case3open':
            rospy.loginfo('True3')

    def check_pos(self,msg):
        while not rospy.is_shutdown():
            rospy.Subscriber('/turtle1/pose',tPose,node.callback_current_pose)
            self.uuid2 = roslaunch.rlutil.get_or_generate_uuid(None, False)
        # case : y reach before x
            if self.current_position[1]< 2 and self.n==0 and self.tstate2!=1:
                    self.n=1
                    self.tstate=1
                    roslaunch.configure_logging(self.uuid2)
                    launch2 = roslaunch.parent.ROSLaunchParent(self.uuid2, ["/home/natta/ws/src/turtle_control/case2.launch"])
                    launch2.start()
            if self.current_position[0]< 2  and self.ispub2=='case2done' and self.n==1:
                    self.n=2
                    roslaunch.configure_logging(self.uuid2)
                    launch2 = roslaunch.parent.ROSLaunchParent(self.uuid2, ["/home/natta/ws/src/turtle_control/case3.launch"])
                    launch2.start()

        # case : x reach before y
            if  self.current_position[0]< 2 and self.n2==0 and self.tstate!=1:
                self.n2=1
                self.tstate2=1
                roslaunch.configure_logging(self.uuid2)
                launch2 = roslaunch.parent.ROSLaunchParent(self.uuid2, ["/home/natta/ws/src/turtle_control/case3.launch"])
                launch2.start()

            if self.current_position[1]< 2  and self.ispub3=='case3open' and self.n2==1:
                self.n2=2
                roslaunch.configure_logging(self.uuid2)
                launch2 = roslaunch.parent.ROSLaunchParent(self.uuid2, ["/home/natta/ws/src/turtle_control/case2.launch"])
                launch2.start()
     
    def callback_shutDownTimer(self):
        self.timer.shutdown()
 


if __name__=='__main__':
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/natta/ws/src/turtle_control/case1.launch"])
    launch.start()

    rospy.loginfo("started")
    rospy.init_node('condition_check')
    node = Node()
    rospy.Subscriber('/openrviz',String,node.check_pub3)
    rospy.Subscriber('/pub2done',String,node.check_pub2)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.check_pos)
    rospy.spin()



