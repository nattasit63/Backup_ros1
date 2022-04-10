#!/usr/bin/env python3

import math
import numpy as np
from multiprocessing.dummy import Array
import rospy
from turtlesim.msg import Pose as tPose
from std_msgs.msg import Int32MultiArray,Bool,String
from std_srvs.srv import Empty, EmptyResponse

#insert_here = [[1.0,1.0],[2.0,5.0]]
pos = [[1,1],[2,5],[8,3],[8,7]]
len_pos = len(pos)

class Node:
    def __init__(self):
        self.isthere = str()
        self.isAtEnd  = str()
        self.timer = None
        self.n =0
        self.flag=0
        self.current_position = np.array([5.5445,5.5445])
        self.goal_position = np.array([0,0])
        self.state =0

    def callback_current_pose(self,msg):
        self.current_position  = np.array([msg.x,msg.y])

    def there(self):
        rospy.Subscriber('/turtle1/pose',tPose,node.callback_current_pose)
        es =[0.1,0.1]
        dp = abs(self.goal_position-self.current_position)
        if dp[0]<=es[0] and dp[1]<=es[1] :
            if self.flag==0:
                self.isthere='True'
                self.flag=1
                rospy.loginfo(self.isthere)
        else:
            self.isthere='False'


    def give_vp(self,events):
       # rospy.Subscriber('/Isthere',String,node.callback_isthere)
        while not rospy.is_shutdown():
            self.there()
            vp = Int32MultiArray()
            vp.data = pos[self.n]
            self.goal_position = vp.data
            pub.publish(vp)
            rospy.loginfo(self.n)
            if self.n<len_pos:
                if self.isthere =='True':
                    self.n=self.n+1
                    vp.data = pos[self.n]
                    self.goal_position = vp.data
                    self.flag=0
                    self.state =2
                    self.isthere = 'False'
                    
                    #pub.publish(vp)
                    #rospy.loginfo(vp)
                else:
                    vp.data = pos[self.n]
                        #self.state=1
                        #rospy.loginfo(self.state)
                        #rospy.loginfo(self.isthere)
                    pub.publish(vp)
            else:
                self.isAtEnd = 'True'
            #else:
              #  break

            #for i in range(0,len(pos)):
                #n=n+1
                #if n<=len(pos):
                # vp.data = pos[i]
                    #rospy.loginfo(vp)
                # pub.publish(vp)
                # rate.sleep()
                #else :
                    #break
    def reset_goal (self,req):		# service method
        self.n=0
        self.flag=0
        self.isthere='False'
        self.isAtEnd = 'False'
        self.goal_position=pos[0]
        self.give_vp(self)
        return EmptyResponse()    

    def callback_shutDownTimer(self):
        self.timer.shutdown()

if __name__ == '__main__':
    node = Node()
    rospy.init_node('viapoint_giver')
    pub = rospy.Publisher('follow_viapoint',Int32MultiArray,queue_size=10)
    re_goal = rospy.Service('/reset_goal',Empty,node.reset_goal)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.give_vp)
    rospy.spin()
