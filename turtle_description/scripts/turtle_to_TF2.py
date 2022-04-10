#!/usr/bin/env python3
import rospy
import tf2_ros as tf
import tf_conversions
from geometry_msgs.msg import PoseStamped, TransformStamped
from std_msgs.msg import Header
from turtlesim.msg import Pose as tPose
import numpy as np
import math
class Node :
    def __init__(self) :
        self.pose = tPose()
        self.pose2 = tPose()
        rospy.init_node('tf_broadcaster')
        rospy.Subscriber('/turtle1/pose',tPose,self.callback_current_pose)
        rospy.Subscriber('/turtle2/pose',tPose,self.callback_current_pose2)
        self.timer = rospy.Timer(rospy.Duration(1.0 / 10), self.tfBroadcasting)
        rospy.on_shutdown(self.callback_shutDownTimer)  
    def callback_current_pose(self,msg):
        self.pose = msg
    def callback_current_pose2(self,msg):
        self.pose2 = msg
    def tfBroadcasting(self,event):
        br = tf.TransformBroadcaster()
        t = TransformStamped()
        h = Header()
        h.stamp = rospy.Time.now()
        h.frame_id = 'world'
        t.header = h
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.pose.x
        t.transform.translation.y = self.pose.y
        t.transform.translation.z = 0.0
        rotation = tf_conversions.transformations.quaternion_from_euler(0,0,self.pose.theta)
        t.transform.rotation.x = rotation[0]
        t.transform.rotation.y = rotation[1]
        t.transform.rotation.z = rotation[2]
        t.transform.rotation.w = rotation[3]
        br.sendTransform(t)

        br2 = tf.TransformBroadcaster()
        t2 = TransformStamped()
        h2 = Header()
        h2.stamp = rospy.Time.now()
        h2.frame_id = 'world'
        t2.header = h
        t2.child_frame_id = 'base_footprint2'
        t2.transform.translation.x = self.pose2.x
        t2.transform.translation.y = self.pose2.y
        t2.transform.translation.z = 0.0
        rotation2 = tf_conversions.transformations.quaternion_from_euler(0,0,self.pose2.theta)
        t2.transform.rotation.x = rotation2[0]
        t2.transform.rotation.y = rotation2[1]
        t2.transform.rotation.z = rotation2[2]
        t2.transform.rotation.w = rotation2[3]
        br2.sendTransform(t2)
    def callback_shutDownTimer(self):
        self.timer.shutdown()
if __name__=='__main__':
    node = Node()
    rospy.spin()
