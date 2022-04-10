#!/usr/bin/env python3
import roslaunch
import rospy
from turtlesim.msg import Pose as tPose
from std_msgs.msg import Int32MultiArray,Bool,String


while(1):

    def callback_state(msg):
        state_get=msg.data


    rospy.Subscriber('/state_publish',String,callback_state)
    rospy.loginfo(state_get)

    if state_get=='1':
        uuid2 = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid2)
        launch2 = roslaunch.parent.ROSLaunchParent(uuid2, ["/home/natta/ws/src/turtle_control/case2.launch"])
        launch2.start()
        n=1




# class Node:
#     def __init__(self):
#         self.timer = None
#         self.n=0
#         self.my_state =0
#         self.state_get =str()
#         self.time_open=0
#         self.pubpos = Int32MultiArray()
#         self.index_word =0
#         self.get_msg = str()
#         self.app=0
#     def callback_state(self,msg):
#         self.state_get=msg.data

#     def map_state(self,event):
#         rospy.Subscriber('/state_publish',String,node.callback_state)
#         rospy.loginfo(self.state_get)
#         if self.state_get=='1':
#             uuid3 = roslaunch.rlutil.get_or_generate_uuid(None, False)
#             roslaunch.configure_logging(uuid3)
#             launch3 = roslaunch.parent.ROSLaunchParent(uuid3, ["/home/natta/ws/src/turtle_control/case2.launch"])
#             launch3.start()
       

#     def callback_shutDownTimer(self):
#         self.timer.shutdown()

# if __name__ == '__main__':
#     node =Node()
#     rospy.init_node('py_map')
    
#     node.timer = rospy.Timer(rospy.Duration(1/10), node.map_state)
#     rospy.spin()
