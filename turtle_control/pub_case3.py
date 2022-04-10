#!/usr/bin/env python3
import numpy as np
import rospy
import roslaunch
from std_msgs.msg import String

        
class Node:
    def __init__(self):
        self.timer = None
        self.n=0
       
    def too(self,event):
        while not rospy.is_shutdown():
            if self.n==0:
                canrun = str()
                canrun = 'case3open' 
                pub.publish(canrun)
                self.n=1
        
    def callback_shutDownTimer(self):
        self.timer.shutdown()
        
if __name__ == '__main__':
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/natta/ws/src/turtle_control/open_rviz.launch"])
    launch.start()
    
    pub = rospy.Publisher('openrviz',String,queue_size=10)
    rospy.loginfo("started")
    rospy.init_node('ll')
    node = Node()
    node.timer = rospy.Timer(rospy.Duration(1/10), node.too)
    rospy.spin()