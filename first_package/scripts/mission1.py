#!/usr/bin/env python3
import math
from turtle import delay
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from turtlesim.msg import Pose as tPose
from std_srvs.srv import Empty, EmptyResponse
class Node :
    def __init__(self):
        self.goal_position = np.array([0,0])
        self.current_position = np.array([0,0])
        self.current_orientation = 0
        self.current_position2 = np.array([0,0])
        self.current_orientation2 = 0
        self.cmd_vel_msg = Twist()
        self.timer = None
    def callback_current_pose(self,msg):
        self.current_position  = np.array([msg.x,msg.y])
        self.current_orientation = msg.theta
    def callback_current_pose2(self,msg):
        self.current_position2  = np.array([msg.x,msg.y])
        self.current_orientation2 = msg.theta

    def control(self):
        dp = self.goal_position-self.current_position2 
        v = 1
        if np.linalg.norm(dp)< 0.1:
            v = 0
        e = math.atan2(dp[1],dp[0])-self.current_orientation2
        K = 10
        w = K*math.atan2(math.sin(e),math.cos(e))
        return v,w

    def publish_cmd_vel(self):
    
        dp = self.goal_position-self.current_position2 
        v,w = self.control()
        self.cmd_vel_msg.linear.x = v
        self.cmd_vel_msg.angular.z = w
        pub_cmd.publish(self.cmd_vel_msg)

    def follow(self,event):
        rospy.Subscriber('/turtle1/pose',tPose,node.callback_current_pose)
        rospy.Subscriber('/turtle3/pose',tPose,node.callback_current_pose2)
        self.goal_position = self.current_position
      
        self.publish_cmd_vel()

    def callback_shutDownTimer(self):
        self.timer.shutdown()


if __name__=='__main__':
    rospy.init_node('target_follower')
    node = Node()
    pub_cmd = rospy.Publisher('turtle3/cmd_vel',Twist,queue_size=10)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.follow)
    #rospy.on_shutdown(node.callback_shutDownTimer)
    rospy.spin()
