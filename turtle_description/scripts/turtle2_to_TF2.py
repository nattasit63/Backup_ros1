#!/usr/bin/env python3
import rospy
import tf2_ros as tf2
import tf_conversions
from geometry_msgs.msg import PoseStamped, TransformStamped
from std_msgs.msg import Header
from turtlesim.msg import Pose as tPose
import numpy as np
import math
class Node :
    def __init__(self) :
        self.pose2 = tPose()
        rospy.init_node('tf_broadcaster2')
        rospy.Subscriber('/turtle/pose',tPose,self.callback_current_pose)
        self.timer = rospy.Timer(rospy.Duration(1.0 / 10), self.tfBroadcasting)
        rospy.on_shutdown(self.callback_shutDownTimer)  
    def callback_current_pose(self,msg):
        self.pose2 = msg
    def tfBroadcasting(self,event):
        br = tf2.TransformBroadcaster()
        t = TransformStamped()
        h = Header()
        h.stamp = rospy.Time.now()
        h.frame_id = 'world'
        t.header = h
        t.child_frame_id = 'base_footprint2'
        t.transform.translation.x = self.pose2.x
        t.transform.translation.y = self.pose2.y
        t.transform.translation.z = 0.0
        rotation = tf_conversions.transformations.quaternion_from_euler(0,0,self.pose2.theta)
        t.transform.rotation.x = rotation[0]
        t.transform.rotation.y = rotation[1]
        t.transform.rotation.z = rotation[2]
        t.transform.rotation.w = rotation[3]
        br.sendTransform(t)
    def callback_shutDownTimer(self):
        self.timer.shutdown()
if __name__=='__main__':
    node = Node()
    rospy.spin()
