#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import json
import os, glob, pathlib
import rospy
import math
from std_msgs.msg import Bool, UInt8
from geometry_msgs.msg import PoseArray, Pose
class Node :
    def __init__(self,node_name):
        self.node_name = node_name
    # initialize node
        rospy.init_node(self.node_name)
    # initialize subscribers
        #rospy.Subscriber('/topic_to_sub',sub_msg_type,self.callback_topic_to_sub)
        #self.sub_msg = sub_msg_type()
    # initialize publishers
        self.pub_via_points = rospy.Publisher('/via_points',PoseArray,queue_size=10)
        self.pub_period = 1
    # assign fixed time publishers 
        self.timer = rospy.Timer(rospy.Duration(self.pub_period), self.publish)
    # assign on_shutdown behavior
        rospy.on_shutdown(self.callback_shutdown)
        self.calculated = False
        self.via_points = None
        self.pos = None
        
    #def callback_topic_to_sub(self,msg):
    #    self.sub_msg = msg
    def publish(self,event):
        if self.calculated:
            via_points_msg = PoseArray()
            for idx in range(len(self.via_points)):
                pose = Pose()
                pose.position.x = self.pos[self.via_points[idx]][0]
                pose.position.y = self.pos[self.via_points[idx]][1]
                via_points_msg.poses.append(pose)
            self.pub_via_points.publish(via_points_msg)
    def callback_shutdown(self):
        print('\n\n... The node "'+self.node_name+'" has shut down...\n')

class GraphLoader:
    def __init__(self,graph_name):
        path = pathlib.Path(__file__).parent.resolve()
        path = os.path.dirname(path)
        file = glob.glob(path+'/**/config.json')
        with open(file[0],"r") as json_data:
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
        
        self.graph = nx.Graph(name=graph_name)
        self.graph.add_nodes_from(dict_nodes.keys())
        for n,p in dict_nodes.items():
            self.graph.nodes[n]['pos'] = p
        for e,d in dict_edges.items():
            self.graph.add_edge(d[0],d[1],weight=euc2d(dict_nodes[d[0]],dict_nodes[d[1]]))
        self.dict_nodes = dict_nodes

def euc2d(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)        
if __name__=="__main__":
    node = Node('graph')
    graph_loader = GraphLoader('Graph Map')
    graph = graph_loader.graph
    node.pos = graph_loader.dict_nodes

    node_start = 4
    node_goal = 11

    pathFound = True
    try:
        node.via_points = nx.astar_path(graph,node_start,node_goal) 
    except nx.NetworkXError as exec:
        pathFound = False
        print(exec)
    if pathFound:
        node.calculated = True
        path = [(0,0)]*(len(node.via_points)-1)
        for i in range(len(node.via_points)-1):
            path[i] = (node.via_points[i],node.via_points[i+1])
        

        nx.draw(graph,pos)
        nx.draw_networkx_edges(graph,pos,path,edge_color="#ff0000",width=4)
        nx.draw_networkx_nodes(graph,pos,via_points,node_color="#ff0000")
        nx.draw_networkx_nodes(graph,pos,[node_start],node_color="#00ff00")
        nx.draw_networkx_nodes(graph,pos,[node_goal],node_color="#0000ff")
        
        plt.show()

        rospy.spin()
