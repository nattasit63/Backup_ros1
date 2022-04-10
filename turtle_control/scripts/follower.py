#!/usr/bin/env python3
import math
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool,Float32,Int32MultiArray,String
from turtlesim.msg import Pose as tPose
from std_srvs.srv import Empty, EmptyResponse

class Node :
    def __init__(self):
        self.goal_position = np.array([0,0])
        self.current_position = np.array([0,0])
        self.current_orientation = 0
        self.cmd_vel_msg = Twist()
        self.timer = None
        self.viapoint = np.array([5.54445,5.54445])


    def callback_current_pose(self,msg):
        self.current_position  = np.array([msg.x,msg.y])
        self.current_orientation = msg.theta
    
    def call_viapoint(self,msg):
        self.viapoint = msg.data
    
    #def endthere(self):
       # tx = 'True'
        #rospy.loginfo(tx)
        #pub_isthere.publish(tx)

    def control(self):
        es =[0.1,0.1]
        dp = self.goal_position-self.current_position
        v = 1
        if np.linalg.norm(dp)< 0.1:
            v = 0
        e = math.atan2(dp[1],dp[0])-self.current_orientation
        K = 10
        w = K*math.atan2(math.sin(e),math.cos(e))
        return v,w

    def publish_cmd_vel(self):
        es =[0.1,0.1]
        dp = self.goal_position-self.current_position
        v,w = self.control()
        self.cmd_vel_msg.linear.x = v
        self.cmd_vel_msg.angular.z = w
        pub_cmd.publish(self.cmd_vel_msg)
    
    def follower(self,msg):
        rospy.Subscriber('/turtle4/pose',tPose,node.callback_current_pose)
        rospy.Subscriber('/follow_viapoint',Int32MultiArray,node.call_viapoint)
        self.goal_position = self.viapoint
        self.publish_cmd_vel()

    def callback_shutDownTimer(self):
        self.timer.shutdown()
 


if __name__=='__main__':
    rospy.init_node('viapoint_follower')
    node = Node()
    #pub_isthere = rospy.Publisher('/Isthere',String,queue_size=10)
    pub_cmd = rospy.Publisher('turtle4/cmd_vel',Twist,queue_size=10)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.follower)
    rospy.spin()
