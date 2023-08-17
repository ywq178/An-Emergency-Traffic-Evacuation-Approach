# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:38:13 2022

@author: ywq
"""

import networkx as nx
import matplotlib.pyplot as plt
#import man
import selfmake
def Grap(t, d, Route):
    # 构建有向图对象
    Map = nx.DiGraph()

    node = selfmake.root.getElementsByTagName('junction')  # 根据标签获取 xml 节点对象集合
    # print(node[0].nodeName)
    pos_location = {}  # position of all nodes in the graph" to draw the figure
    loc = []
    for i in range(len(node)):
        if node[i].getAttribute('type') != 'internal' and node[i].getAttribute('type') != 'unregulated':
            ID = node[i].getAttribute('id')
            lat = float(node[i].getAttribute('x'))
            lon = float(node[i].getAttribute('y'))
            #     print(ID, lat, lon)

            Map.add_node(ID
                         , ID=ID
                         , lat=lat
                         , lon=lon
                         )
            pos_location[ID] = (lon, lat)
            loc.append([lon, lat])

    way_set = selfmake.root.getElementsByTagName('edge')
    # print(way_set[0].nodeName)

    for i in range(len(way_set)):
        # print(way_set[i].getAttribute('id'),way_set[i].getAttribute('function'))
        if way_set[i].getAttribute('function') != 'internal':
            # print(way_set[i].getAttribute('id'))
            ID = way_set[i].getAttribute('id')
            fro = way_set[i].getAttribute('from')
            to = way_set[i].getAttribute('to')
            a = way_set[i].getElementsByTagName('lane')
            length = float(a[0].getAttribute('length'))
            # print(length)
            # print(lane_set[i].getAttribute('length'))
            #     print(ID, lat, lon)
            Map.add_weighted_edges_from([(fro, to, length)])

    Del_Route=[]
    #print('start')
    for i in range(len(Route)):
        #print(list(Map.predecessors(Route[i][0])), type(list(Map.predecessors(Route[i][0]))),len(list(Map.predecessors(Route[i][0]))))
        #print(list(Map.successors(Route[i][0])), len(list(Map.predecessors(Route[i][0]))))
        #print(Route[i],Route[i][0],list(Map.predecessors(Route[i][0])),list(Map.successors(Route[i][0])))
        if (len(list(Map.predecessors(Route[i][1]))) != 1 or len(list(Map.successors(Route[i][1]))) != 1) and (len(list(Map.predecessors(Route[i][0]))) != 1 or len(list(Map.successors(Route[i][0]))) != 1):
            Del_Route.append((Route[i][0], Route[i][1]))
    #print('End')
    for i in range(len(Del_Route)):
        # print(Route[i],type(Route[i]))
        Map.remove_edge(Del_Route[i][0], Del_Route[i][1])  # 删除边
    # print(list(Map.edges()))

    '''
    pos = nx.spiral_layout(G)
    nx.draw(G,pos,with_labels=True,node_size=500,node_color='#7FFF00')#在这里添加属性，添加颜色和大小
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    plt.show() 
    '''
    minWPath2 = nx.dijkstra_path(Map, source=t, target=d)  # 顶点 0 到 顶点 17 的最短加权路径
    lMinWPath2 = nx.dijkstra_path_length(Map, source=t, target=d)  # 最短加权路径长度
    ##print(minWPath2)
    # print(lMinWPath2)
    return minWPath2
