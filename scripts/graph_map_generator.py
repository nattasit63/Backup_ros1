#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import json
import yaml
import os, glob, pathlib
import math
import pygame
from pygame.locals import *
import numpy as np
import rospy
class Node :
    def __init__(self,node_name):
        self.node_name = node_name
    # initialize node
        rospy.init_node(self.node_name)
    # initialize subscribers
        #rospy.Subscriber('/topic_to_sub',sub_msg_type,self.callback_topic_to_sub)
        #self.sub_msg = sub_msg_type()
    # initialize publishers
        #self.pub_via_points = rospy.Publisher('/via_points',PoseArray,queue_size=10)
        #self.pub_period = 1
    # assign fixed time publishers 
        #self.timer = rospy.Timer(rospy.Duration(self.pub_period), self.publish)
    # assign on_shutdown behavior
        rospy.on_shutdown(self.callback_shutdown)
        #self.calculated = False
        #self.via_points = None
        #self.pos = None
        
    #def callback_topic_to_sub(self,msg):
    #    self.sub_msg = msg
    #def publish(self,event):
        #pass
    def callback_shutdown(self):
        print('\n\n... The node "'+self.node_name+'" has shut down...\n')

def euc2d(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

class MapLoader:
    def __init__(self):
        path = pathlib.Path(__file__).parent.resolve()
        self.path = os.path.dirname(path)
        map_file = glob.glob(self.path+'/maps/*.yaml')[0]
        with open(map_file, "r") as stream:
            try:
                self.map_info = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.file = glob.glob(self.path+'/**/'+self.map_info['image'])[0]
class GUI:
    size_screen_initial = [500,500]
    def __init__(self,file_img):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size_screen_initial,HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.pic = pygame.image.load(file_img)       
    def draw_map(self,graph):
        size_screen = self.screen.get_size()
        size_pic = self.pic.get_size()
        ar_pic = size_pic[0]/size_pic[1]
        ar_screen = size_screen[0]/size_screen[1]
        width_button = 150
        if ar_pic+width_button/size_screen[1]>=ar_screen:
            size = [size_screen[0]-width_button,(size_screen[0]-width_button)/ar_pic]
            pos = [0,(size_screen[1]-size[1])/2]
        else:
            size = [ar_pic*size_screen[1],size_screen[1]]
            pos = [(size_screen[0]-size[0]-width_button)/2,0]
        
        H_I_O = np.array([[1,0,0,pos[0]],[0,-1,0,pos[1]+size[1]],[0,0,-1,0],[0,0,0,1]])
        c = math.cos(graph.origin[2])
        s = math.sin(graph.origin[2])
        p = np.array(graph.origin[0:2])
        r = graph.resolution
        ratio = size[0]/size_pic[0]
        H_M_O = np.array([[c,-s,0,(p[0]/r)*ratio],[s,c,0,(p[1]/r)*ratio],[0,0,1,0],[0,0,0,1]])
        H_I_M = np.matmul(H_I_O,np.linalg.inv(H_M_O))
        x_color = (255,0,0)
        y_color = (0,255,0)
        p_origin = H_I_M[0:2,3]
        axis_length = 25
        p_x = p_origin + axis_length*H_I_M[0:2,0]
        p_y = p_origin + axis_length*H_I_M[0:2,1]
        if size_screen[0]>width_button:
            #p_origin = [int(p) for p in p_origin]
            self.screen.blit(pygame.transform.scale(self.pic,  [int(s) for s in size]), [int(p) for p in pos])
            pygame.draw.line(self.screen,x_color,[int(o) for o in p_origin],[int(x) for x in p_x],3)
            pygame.draw.line(self.screen,y_color,[int(o) for o in p_origin],[int(y) for y in p_y],3)
            pygame.display.flip()
    def draw_graph(self,graph):
        size_screen = self.screen.get_size()
        size_pic = self.pic.get_size()
        ar_pic = size_pic[0]/size_pic[1]
        ar_screen = size_screen[0]/size_screen[1]
        width_button = 150
        if ar_pic+width_button/size_screen[1]>=ar_screen:
            size = [size_screen[0]-width_button,(size_screen[0]-width_button)/ar_pic]
            pos = [0,(size_screen[1]-size[1])/2]
        else:
            size = [ar_pic*size_screen[1],size_screen[1]]
            pos = [(size_screen[0]-size[0]-width_button)/2,0]
        H_I_O = np.array([[1,0,0,pos[0]],[0,-1,0,pos[1]+size[1]],[0,0,-1,0],[0,0,0,1]])
        c = math.cos(graph.origin[2])
        s = math.sin(graph.origin[2])
        p = np.array(graph.origin[0:2])
        r = graph.resolution
        ratio = size[0]/size_pic[0]
        H_M_O = np.array([[c,-s,0,(p[0]/r)*ratio],[s,c,0,(p[1]/r)*ratio],[0,0,1,0],[0,0,0,1]])
        H_I_M = np.matmul(H_I_O,np.linalg.inv(H_M_O))
        dict_nodes = nx.get_node_attributes(graph,'pos')

        node_color = (255,0,0)
        node_radius = 0.05
        edge_color = (0,0,255)
        edge_width = 3
        for e in graph.edges:
            p_1 = np.array(dict_nodes[e[0]])/r*ratio
            p_2 = np.array(dict_nodes[e[1]])/r*ratio

            p_transform_1 = np.matmul(H_I_M,np.array([[p_1[0]],[p_1[1]],[0],[1]]))
            p_transform_2 = np.matmul(H_I_M,np.array([[p_2[0]],[p_2[1]],[0],[1]]))

            pygame.draw.line(self.screen,edge_color,[p_transform_1[0][0],p_transform_1[1][0]],[p_transform_2[0][0],p_transform_2[1][0]],width=edge_width)
        for n,p in dict_nodes.items():
            p_new = (np.array(p)/r)*ratio
            p_transform = np.matmul(H_I_M,np.array([[p_new[0]],[p_new[1]],[0],[1]]))
            node_pos = [p_transform[0][0],p_transform[1][0]]
            pygame.draw.circle(gui.screen,node_color,node_pos,node_radius/r*ratio)
            pygame.display.flip()        
class GraphMap(nx.Graph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
    # load map from YAML
        map_loader = MapLoader()
        self.image_file = map_loader.file
        self.image = map_loader.map_info['image']
        self.resolution = map_loader.map_info['resolution']
        self.origin = map_loader.map_info['origin']
        self.occupied_thresh = map_loader.map_info['occupied_thresh']
        self.free_thresh = map_loader.map_info['free_thresh']
        self.negate = map_loader.map_info['negate']
    # load graph from JSON
        path = pathlib.Path(__file__).parent.resolve()
        path = os.path.dirname(path)
        graph_file = glob.glob(path+'/**/config.json')
        with open(graph_file[0],"r") as json_data:
            try:
                data = json.load(json_data)
            except json.JSONDecodeError as exec:
                print(exec)
        dict_nodes = {}
        dict_edges = {}
        
        for n,p in data['nodes'].items():
            dict_nodes[int(n)] = tuple(p)
        for e,d in data['edges'].items():
            dict_edges[int(e)] = tuple(d)
        
        self.add_nodes_from(dict_nodes.keys())
        for n,p in dict_nodes.items():
            self.nodes[n]['pos'] = p
        for e,d in dict_edges.items():
            self.add_edge(d[0],d[1],weight=euc2d(dict_nodes[d[0]],dict_nodes[d[1]]))

# main
if __name__=="__main__":
    node = Node('graph')

    graph = GraphMap(name='Graph Map')
    gui = GUI(graph.image_file)
    gui.draw_map(graph)
    gui.draw_graph(graph)
    inGame = True
    while inGame:
        for event in pygame.event.get():
            if event.type == QUIT: 
                inGame = False
            elif event.type == VIDEORESIZE:
                gui.draw_map(graph)
                gui.draw_graph(graph)
    rospy.spin()

