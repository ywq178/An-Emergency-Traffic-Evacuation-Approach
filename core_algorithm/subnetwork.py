# author: Weiqi Yu
# 开发时间: 2022/11/16 9:44
"一个路网（.net）所有路段的子网"
import networkx as nx
import matplotlib.pyplot as plt
import copy
import man
import time

start = time.perf_counter()
# 构建有向图对象
Map = nx.DiGraph()

node = man.root.getElementsByTagName('junction') # 根据标签获取 xml 节点对象集合
#print(node[0].nodeName)
pos_location = {}  # position of all nodes in the graph" to draw the figure
loc = []
for i in range(len(node)):
   if node[i].getAttribute('type')!='internal' and node[i].getAttribute('type')!='unregulated':
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

way_set = man.root.getElementsByTagName('edge')
# print(way_set[0].nodeName)

for i in range(len(way_set)):
   #print(way_set[i].getAttribute('id'),way_set[i].getAttribute('function'))
   if way_set[i].getAttribute('function')!='internal':
    #print(way_set[i].getAttribute('id'))
    ID = way_set[i].getAttribute('id')
    fro = way_set[i].getAttribute('from')
    to = way_set[i].getAttribute('to')
    a = way_set[i].getElementsByTagName('lane')
    length = float(a[0].getAttribute('length'))
    #print(length)
    #print(lane_set[i].getAttribute('length'))
    #     print(ID, lat, lon)
    #Map.add_weighted_edges_from([(fro, to, length, ID)])
    Map.add_edge(fro, to, weight=length, id=ID)

nodes = list(Map.nodes()) #遍历所有节点
edges = list(Map.edges()) #遍历边

# 先寻找路网的边缘节点
edge_nodes = []  # 储存边缘节点
for i in range(0, len(nodes)):
    if list(Map.predecessors(str(nodes[i]))) == []:
        edge_nodes.append(str(nodes[i]))
#print(edge_nodes)

#edges_name=[[] for x in range(len(edges))]
#sub_name=[[] for x in range(len(edges))]

for i in range(len(edges)):
    print(edges[i])#边的from和to
    #print(edges[i][0],edges[i][1])
    #print(Map[edges[i][0]][edges[i][1]]['id']) #边的ID
    t = edges[i][0] #指向
    d = edges[i][1] #被指向

#t=str(input('头节点:'))
#d=str(input('尾节点：'))

    # 将边缘节点的基础上，寻找它们到头节点的最短路径上的所有节点。
    sub_nodes = []
    for i in range(0,len(edge_nodes)):
      if nx.has_path(Map, edge_nodes[i], t) == True:
        cd = [p for p in nx.all_shortest_paths(Map, source=edge_nodes[i], target=t, weight='weight')]
        for x in range(len(cd)):
            for y in range(len(cd[x])):
                if sub_nodes != []:
                    o = 0
                    for j in range(len(sub_nodes)):
                        if cd[x][y] == sub_nodes[j]:
                            o = o + 1
                    if o == 0:
                        sub_nodes.append(str(cd[x][y]))
                else:
                    sub_nodes.append(str(cd[x][y]))
    #sub_nodes=natsorted(sub_nodes)  # 重新排序
    #print(sub_nodes,type(sub_nodes))

    # 储存sub_nodes数组中节点到头节点和尾节点的最短路径及其长度。储存为一级抽取子网节点（整个子网）
    tt = [[] for x in range(len(nodes))]  # 所有节点到头节点（指向）的路径
    tt_length = [[] for x in range(len(nodes))]  # 路径长
    dd = [[] for x in range(len(nodes))]  # 所有节点到尾节点（被指向）的路径
    dd_length = [[] for x in range(len(nodes))]  # 路径长
    # print(len(tt))
    # print(dd)

    # 头节点t
    for i in range(len(sub_nodes)):
        if sub_nodes[i] != t:
            if nx.has_path(Map, sub_nodes[i], str(t)) == True:  # 查看i到t的路径是否存在
                pos=nodes.index(sub_nodes[i])
                # print('计算图中节点'+str(sub_nodes[i])+'到节点'+str(t)+'的所有最短路径: ',[p for p in nx.all_shortest_paths(G, source=sub_nodes[i], target=t, weight='weight')])
                # print('计算图中节点'+str(sub_nodes[i])+'到节点'+str(t)+'的所有最短路径的长度: ',nx.shortest_path_length(G, source=sub_nodes[i], target=t, weight='weight'))
                tt_length[pos].append(nx.shortest_path_length(Map, source=sub_nodes[i], target=str(t), weight='weight'))  # 储存最短路径长度
                cd = [p for p in nx.all_shortest_paths(Map, source=sub_nodes[i], target=str(t), weight='weight')]  # 最短路径
                for x in range(len(cd)):
                    for y in range(len(cd[x])):
                        tt[pos].append(cd[x][y])  # 储存i到t的最短路径
            else:
                print("wu")  # 不存在路径输出“无”
    #print(tt)
    #print(tt_length)

    # 同理，尾节点d
    for i in range(len(sub_nodes)):
        if sub_nodes[i] != d:
            if nx.has_path(Map, sub_nodes[i], str(d)) == True:
                pos=nodes.index(sub_nodes[i])
                # print('计算图中节点'+str(sub_nodes[i])+'到节点'+str(d)+'的所有最短路径: ',[p for p in nx.all_shortest_paths(G, source=sub_nodes[i], target=d, weight='weight')])
                # print('计算图中节点'+str(sub_nodes[i])+'到节点'+str(d)+'的所有最短路径的长度: ',nx.shortest_path_length(G, source=sub_nodes[i], target=d, weight='weight'))
                dd_length[pos].append(nx.shortest_path_length(Map, source=sub_nodes[i], target=str(d), weight='weight'))
                cd = [p for p in nx.all_shortest_paths(Map, source=sub_nodes[i], target=str(d), weight='weight')]
                for x in range(len(cd)):
                    for y in range(len(cd[x])):
                        dd[pos].append(cd[x][y])
            else:
                print("wu")
    #print(dd)
    #print(dd_length)

    for i in range(len(nodes)):
        if tt_length[i] > dd_length[i]:
            tt[i] = []

    for i in range(0, len(nodes)):
        b = 0
        c = 0
        ps = list(Map.predecessors(str(nodes[i])))
        for j in range(len(ps)):
            b = b + 1
            a = ps[j]
            pos1 = nodes.index(ps[j])
            if dd_length[i] > dd_length[pos1] or dd_length[pos1] == []:# a not in sub_nodes
                c = c + 1
        if b == c != 0:
            tt[i] = []
    #删除3
    v = []
    for i in range(len(tt)):
        if tt[i] != []:
            v.append(tt[i][0])
    # print(v)
    vv = []
    for i in range(len(v)):
        if list(Map.predecessors(str(v[i]))) == []:
            vv.append(str(v[i]))
    # print(vv)
    vvv = []
    for i in range(0, len(vv)):
        if nx.has_path(Map, vv[i], t) == True:
            cd = [p for p in nx.all_shortest_paths(Map, source=vv[i], target=t, weight='weight')]
            for x in range(len(cd)):
                for y in range(len(cd[x])):
                    if vvv != []:
                        o = 0
                        for j in range(len(vvv)):
                            if cd[x][y] == vvv[j]:
                                o = o + 1
                        if o == 0:
                            vvv.append(str(cd[x][y]))
                    else:
                        vvv.append(str(cd[x][y]))
    for i in range(len(v)):
        p=nodes.index(v[i])
        if v[i] not in vvv:
            tt[p]=[]
    print(tt)

    edge_sub=[]
    for i in range(len(tt)): #子网的边
        for j in range(len(tt[i])):
            if j<len(tt[i])-1:
              edge_sub.append((tt[i][j],tt[i][j+1]))
    #print(edge_sub)

    # 储存二级子网
    w = []
    for i in range(len(tt)):
        for j in range(len(tt[i])):
            w.append(tt[i][j])
    k = Map.subgraph(w)
    l = k.subgraph(nodes).copy()
    #print(list(l.edges()))  # 遍历边

    for i in range(len(list(k.edges()))):
        if list(k.edges())[i] not in edge_sub:
            #l.remove_edges_from([('10','26')])
            l.remove_edges_from([list(k.edges())[i]])
    #储存
    #nx.write_weighted_edgelist(l, "D:\pythonProject\subnet\subnetwork{}-{}".format(t,d))
    nx.write_weighted_edgelist(l, "D:\\pythonProject\\subnet\\{}-{}".format(t, d))

    #print(edges_name)
    #print(sub_name)
'''
    plt.rcParams['figure.figsize'] = (20, 20)  # 单位是inches
    plt.title((t,d))
    nx.draw(l
            , pos=pos_location
            , with_labels = True
            , node_size=500
            , node_color='#7FFF00'
            # '#FF8000' #'#6DCAF2' # '#FF8000' # '#6DCAF2' #  '#B9F1E5'   #'grey'   # '#FFBFBF' #  'k' #nodes_col.values()   #'y'
            , width=0.5  # default = 1.0 , Line width of edges
            #         , font_size = 4
            #         , font_family = 'arial'
            , edge_color='grey'  # b, k, m, g,
            )
    # fig_name = 'result_figures/manhattan_map_dpi200.jpg'
    
    # plt.savefig(fig_name, dpi=200)
    labels = nx.get_edge_attributes(l, length)
    nx.draw_networkx_edge_labels(l, pos=pos_location, edge_labels = labels)
    plt.show()
'''