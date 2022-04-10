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
        self.input_box = pg.Rect(200,200,140,32)
        self.color = pg.Color('lightskyblue3')
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption('planning')
        # self.font = pg.font.SysFont("Cordia New",30,True,False)


    def clearscreen(self):
        self.screen.fill((0,0,0))
        pg.display.update()

    def buildtext(self,text,posx,posy):
        pos=(posx,posy)
        self.screen.blit(font.render(str(text),True, (255 ,255 ,255)),pos)
        pg.display.update()

    def drawbox(self):
        pg.draw.rect(self.screen,self.color,self.input_box,2)

    def checkstate(self):
        self.clearscreen()
        self.buildtext(self.my_state,20,20)

    def callback_senddone(msg,self):
        self.get_msg = msg.data



    def state_check(self,events):
        
        if self.my_state==0:
            surface = font.render("Planning",True, (255 ,255 ,255))
            self.screen.blit(surface,(50,50))
            self.buildtext('Please select path ',50,150)
            self.buildtext('a = [4,5],[1,5],[2,2] ',70,200)
            self.buildtext('b = [6,3],[3,6],[5,7] ',70,250)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.key == pg.K_a:
                        self.my_state=1
                    elif event.key == pg.K_b:
                        self.my_state=2
                    else:
                        self.buildtext('Error , Input again',200,400)
                        self.time_open=0
                        self.my_state=0                   
        elif self.my_state==1:
            pub_state = String()
            pub_state.data = 'a'
            pub.publish(pub_state) 
            pg.quit()

        elif self.my_state==2:
            pub_state = String()
            pub_state.data = 'b'
            pub.publish(pub_state) 
            pg.quit()
        else :
            self.buildtext('error ,select again',50,150)
            self.my_state=0

    def callback_shutDownTimer(self):
        self.timer.shutdown()

if __name__ == '__main__':
    rospy.loginfo("started")
    node =Node()
    rospy.init_node('plan')
    pg.init()
    pg.font.init()
    font = pg.font.SysFont("Cordia New",30,True,False)
    pub=rospy.Publisher('path_select',String,queue_size=10)
    node.timer = rospy.Timer(rospy.Duration(1/10), node.state_check)
    rospy.spin()
