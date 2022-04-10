#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import json
import os, glob, pathlib
import rospy
import math
from std_msgs.msg import Bool, UInt8

class Node :
    def __init__(self,node_name):
        self.node_name = node_name
        rospy.init_node(self.node_name)
        # Set up the drawing window
        #rospy.Subscriber('/topic_to_sub',sub_msg_type,self.callback_topic_to_sub)
        #self.pub_topic_to_pub = rospy.Publisher('/topic_to_pub',pub_msg_type,queue_size=50)
        #self.sub_msg = sub_msg_type()
        self.pub_period = 0.1 
        #self.timer = rospy.Timer(rospy.Duration(self.pub_period), self.publish)
        rospy.on_shutdown(self.callback_shutdown)
        
    #def callback_topic_to_sub(self,msg):
    #    self.sub_msg = msg
    #def publish(self,event):
        #topic_to_pub_msg = pub_msg_type()

        #self.pub_topic_to_pub = topic_to_pub_msg
    def callback_shutdown(self):
        print('\n\n... The node "'+self.node_name+'" has shut down...\n')

class GraphLoader:
    def __init__(self):
        path = pathlib.Path(__file__).parent.resolve()
        path = os.path.dirname(path) 
        self.file = glob.glob(path+'/**/config.json')
        self.load()
    def load(self):
        with open(self.file[0], "r") as json_data:
            try:
                data = json.load(json_data)
            except json.JSONDecodeError as exc:
                print(exc)
        self.pos = {}
        self.edge_data = {}
        for n,p in data['nodes'].items():
            self.pos[int(n)] = tuple(p)
        for e,d in data['edges'].items():
            self.edge_data[int(e)] = tuple(d)
def euc2d(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    # return 1

if __name__=="__main__":
    node = Node('graph')
    graph_info = GraphLoader()
    pos = graph_info.pos
    edge_data = graph_info.edge_data
    graph = nx.Graph(name="Graph Map")
    graph.add_nodes_from(pos.keys())

    for n, p in pos.items():
        graph.nodes[n]['pos'] = p
    for e,d in edge_data.items():
        graph.add_edge(d[0],d[1],weight=euc2d(graph.nodes[d[0]]['pos'],graph.nodes[d[1]]['pos']))
    start_node = 5
    goal_node = 8
    pathFound = True
    try:
        via_points = nx.astar_path(graph,start_node,goal_node)
    except nx.NetworkXError as exec:
        pathFound = False
        print(exec)

    if pathFound:
        path = [(0,0)]*len(via_points)
        for i in range(len(via_points)-1):
            path[i] = (via_points[i],via_points[i+1])
        nx.draw(graph,pos)
        nx.draw_networkx_edges(graph,pos,path,edge_color="r",width=3)
        nx.draw_networkx_nodes(graph,pos,via_points,node_color="#ff0000")
        nx.draw_networkx_nodes(graph,pos,[start_node],node_color="#00ff00")
        nx.draw_networkx_nodes(graph,pos,[goal_node],node_color="#0000ff")
        plt.show()
        rospy.spin()