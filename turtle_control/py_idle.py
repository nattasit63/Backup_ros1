#!/usr/bin/env python3
from ast import Str
import pygame as pg
import roslaunch
import rospy
from turtlesim.msg import Pose as tPose
from std_msgs.msg import Int32MultiArray,Bool,String,Int8
import subprocess
import time

class Node:
    def __init__(self):
        self.timer = None
        self.n=0
        self.my_state =0
        
        self.time_open=0
        self.pubpos = Int32MultiArray()
        self.index_word =0
        self.get_msg = str()
        self.is2done = str()
        self.app=0
        height = 600
        width = 800
        self.path = str()
        self.color = pg.Color('lightskyblue3')
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption('IDLE')
        # self.font = pg.font.SysFont("Cordia New",30,True,False)


    def clearscreen(self):
        self.screen.fill((0,0,0))
        pg.display.update()

    def buildtext(self,text,posx,posy):
        pos=(posx,posy)
        self.screen.blit(font.render(str(text),True, (255 ,255 ,255)),pos)
        pg.display.update()


    def checkstate(self):
        self.clearscreen()
        self.buildtext(self.my_state,20,20)

    def callback_senddone(msg,self):
        self.get_msg = msg.data

    def callback_case2(self,msg):
        self.is2done = msg.data

    def callback_path(self,msg):
        self.path = msg.data

    def state_check(self,events):
        if self.my_state==0:
            surface = font.render("Mapping  ",True, (255 ,255 ,255))
            self.screen.blit(surface,(50,50))
            self.buildtext('Please select launch file ',50,150)
            self.buildtext('q = turtle viapoint follower ',70,200)
            self.buildtext('w = rviz ',70,250)
            # buildtext('w = rviz ',90,200)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.my_state=1
                    
                    else:
                        self.buildtext('Error , Input again',200,400)
                        self.time_open=0
                        self.my_state=0                   
                        
        elif self.my_state==1:
            if self.time_open!=1:
                self.time_open=1
                self.clearscreen()
                self. buildtext('Are you sure to select "q"?  [y/n]',200,300)
                # checkstate()
            if self.time_open==1:
                for events in pg.event.get():
                    if events.type == pg.KEYDOWN:
                        if events.type == pg.QUIT:
                            run = False
                            pg.quit()
                        elif events.key == pg.K_y:
                            self.time_open=0
                            self.my_state=3
                            self.clearscreen()
                        elif events.key == pg.K_n:
                            self.time_open=0
                            self.clearscreen()
                            self.my_state=0
                        else:
                            self.time_open=0
                            self.buildtext('Error2 , Input again',200,400)
                            self.my_state=1

        elif self.my_state==2:
            rospy.Subscriber('/pub2done',String,node.callback_case2)
            
            if self.time_open==0:
                self.clearscreen()
                self.checkstate()
                for events in pg.event.get():
                    if events.type == pg.KEYDOWN:
                        if events.type == pg.QUIT:
                            run = False
                            pg.quit()
                pub_state = String()
                pub_state.data = '1'
                pub2.publish(pub_state) 
                time.sleep(3)
                self.time_open=2 
            elif self.time_open==2:    
                if self.path=='a':
                    wordd = [[4,5],[1,5],[2,2]]
                    len_word = len(wordd)
                    pub3.publish(len_word)
                    if self.index_word<=len(wordd)-1:
                        self.pubpos.data = wordd[self.index_word]
                        pub.publish(self.pubpos)
                        self.index_word+=1
                        self.my_state=2
                    if self.is2done=='case2done':
                        self.time_open=0
                        self.clearscreen()
                        time.sleep(3)
                        self.my_state=0
                        
                if self.path=='b':
                    wordd = [[6,3],[3,6],[5,7]]
                    len_word = len(wordd)
                    pub3.publish(len_word)
                    if self.index_word<=len(wordd)-1:
                        self.pubpos.data = wordd[self.index_word]
                        pub.publish(self.pubpos)
                        self.index_word+=1
                        self.my_state=2
                    if self.is2done=='case2done':
                        self.time_open=0
                        self.clearscreen()
                        time.sleep(3)
                        self.my_state=0

        elif self.my_state==3:
            rospy.Subscriber('/path_select',String,node.callback_path)
            if self.time_open==0:
                self.clearscreen()
                # self.checkstate()
                package = 'turtle_control'
                launch_file2 = 'launch_planning.launch'
                command2 = "roslaunch  {0} {1}".format(package, launch_file2)
                subprocess.Popen(command2, shell=True)
                for events in pg.event.get():
                    if events.type == pg.KEYDOWN:
                        if events.type == pg.QUIT:
                            run = False
                            pg.quit()
                self.time_open=1
            if self.time_open==1:
                if self.path=='a' or self.path=='b':
                    self.my_state=2
                    self.time_open=0
                    self.clearscreen()
                # self.my_state=2
                # self.clearscreen()


    def callback_shutDownTimer(self):
        self.timer.shutdown()

if __name__ == '__main__':
    package = 'turtle_control'
    launch_file = 'mapping.launch'
    command = "roslaunch  {0} {1}".format(package, launch_file)
    subprocess.Popen(command, shell=True)
    
    rospy.loginfo("started")
    node =Node()
    rospy.init_node('idle')
    pub=rospy.Publisher('idle_viapoint',Int32MultiArray,queue_size=10)
    pub2=rospy.Publisher('state_publish',String,queue_size=10)
    pub3=rospy.Publisher('len_word',Int8,queue_size=10)
    pg.init()
    pg.font.init()
    font = pg.font.SysFont("Cordia New",30,True,False)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.state_check)
    rospy.spin()
