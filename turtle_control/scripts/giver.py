#!/usr/bin/env python3
import math
import numpy as np
from multiprocessing.dummy import Array
import rospy
from turtlesim.msg import Pose as tPose
from std_msgs.msg import Int32MultiArray,Bool,String,Int8
from std_srvs.srv import Empty, EmptyResponse


# pos = [[1,1],[1,5],[4,5],[8,4]]
# len_pos = len(pos)

class Node:
    def __init__(self):
        self.isthere = str()
        self.isAtEnd  = str()
        self.timer = None
        self.timer2 = None
        self.n =0
        self.flag=0
        self.current_position = np.array([5.5445,5.5445])
        self.goal_position = np.array([0,0])
        self.lastpose = np.array([8,4])
        self.state =0
        self.tod=0
        self.vp= Int32MultiArray()
        self.pos=[]
        self.collect=[]
        self.get=0
        self.pre_vp=[]
        self.len =0
    def callback_current_pose(self,msg):
        self.current_position  = np.array([msg.x,msg.y])

    def callback_viapoint(self,msg):
        self.collect = msg.data
    def callback_len(self,msg):
        self.len = msg.data

    def call_viapoint(self,msg):
        # rospy.loginfo(self.pos)
        rospy.Subscriber('/idle_viapoint',Int32MultiArray,node.callback_viapoint)
        rospy.Subscriber('/len_word',Int8,node.callback_len)
        if len(self.collect)==2 :
            # self.pre_vp=self.collect
            # rospy.loginfo(self.collect)
            self.collect_via()

    def collect_via(self):
        if len(self.collect)!=0 :
            self.pos.append(self.collect)

            if len(self.pos)==self.len:
                rospy.loginfo(self.pos)
                self.give_vp()
            

    def there(self):
        rospy.Subscriber('/turtle4/pose',tPose,node.callback_current_pose)
        es =[0.1,0.1]
        dp = abs(self.goal_position-self.current_position)
        if dp[0]<=es[0] and dp[1]<=es[1] :
            if self.flag==0:
                self.isthere='True'
                self.flag=1
        else:
            self.isthere='False'


    def give_vp(self):
        while not rospy.is_shutdown():
                pos = self.pos
                self.there()
                self.qq()
                self.vp = Int32MultiArray()
                self.vp.data = pos[self.n]
                self.goal_position = self.vp.data
                pub.publish(self.vp)
  
                len_pos = len(pos)
                if self.n<len_pos:
                    if self.isthere =='True':
                        self.n=self.n+1
                        if self.n>=len_pos:
                            self.n=len_pos-1
                        self.vp.data = pos[self.n]
                        self.goal_position = self.vp.data
                        self.flag=0
                        self.state =2
                        self.isthere = 'False'
                    else:
                        self.vp.data = pos[self.n]
                        pub.publish(self.vp)
                else:
                    self.n=len_pos-1
                    self.isAtEnd = 'True'

    def qq (self):
        es =[1,1]
        dp = abs(self.lastpose-self.current_position)
        # if dp[0]<=es[0] and dp[1]<=es[1] and self.tod==0 and self.n==self.len-1:	
        #     self.tod=1
        #     canrun = str()
        #     canrun = 'case2done' 
        #     pub2.publish(canrun)
        if self.n==self.len-1:
            if self.tod==0 :
                canrun = str()
                canrun = 'case2done' 
                pub2.publish(canrun)
                self.tod=1
        # canrun = str()
        # canrun = 'case2done' 
        # pub2.publish(canrun)
            
    def reset_goal (self,req):		
        self.n=0
        self.flag=0
        self.isthere='False'
        self.isAtEnd = 'False'
        self.goal_position=self.pos[0]
        self.give_vp(self)
        return EmptyResponse()    
    
   
    def callback_shutDownTimer(self):
        self.timer.shutdown()
    def callback_shutDownTimer(self):
        self.timer2.shutdown()


if __name__ == '__main__':
    node = Node()
    rospy.init_node('viapoint_giver')
    pub = rospy.Publisher('follow_viapoint',Int32MultiArray,queue_size=10)
    pub2 = rospy.Publisher('pub2done',String,queue_size=10)

    re_goal = rospy.Service('/reset_goal',Empty,node.reset_goal)
    # node.timer = rospy.Timer(rospy.Duration(1/10), node.give_vp)
    node.timer2 =  rospy.Timer(rospy.Duration(1/10), node.call_viapoint)
    rospy.spin()
