# author: Weiqi Yu
# 开发时间: 2022/10/25 20:30
# author: Weiqi Yu
# 开发时间: 2022/10/20 17:01
import networkx as nx
import matplotlib.pyplot as plt
import copy
import man
import time
from natsort import natsorted
def Grap(t,d,Travel_Distance):
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
        Map.add_weighted_edges_from([(fro, to, length)])
    '''
        Map.add_edge(fro, to
                     , way_type=0
                     )
    '''


    nodes = list(Map.nodes())
    #print(nodes,nodes[1],type(nodes[1]))
    #print(len(nodes))
    # 输入
    #t=str(input('头节点:'))
    #d=str(input('尾节点：'))
    #Travel_Distance=int(input('疏散距离:'))

    # 先寻找路网的边缘节点
    edge_nodes = []  # 储存边缘节点
    for i in range(0, len(nodes)):
        if list(Map.predecessors(str(nodes[i]))) == []:
            edge_nodes.append(str(nodes[i]))
    #print(edge_nodes)
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
    #print(sub_nodes)

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
    start = time.perf_counter()
    # 储存二级抽取子网节点（一级子网的子网）,删除不经过路段t->d就可以更快到达节点d的节点及其路径
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

    for i in range(len(nodes)):
        if tt_length[i] > dd_length[i]:
            tt[i] = []
    # print(tt)

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
    # print(vvv)

    # 储存二级子网
    w = []
    for i in range(len(tt)):
        for j in range(len(tt[i])):
            w.append(tt[i][j])
    k = Map.subgraph(w)
    #print(list(k.nodes),list(k.edges))
    #print(len(list(k.nodes)))

    # 提取三级子网,再次寻找二级子网下的边缘节点
    set_c = set(list(k.nodes)) & set(edge_nodes)
    edge_nodes1 = list(set_c)
    #edge_nodes1=natsorted(edge_nodes1)  # 重新排序
    #print(edge_nodes1)

    # 根据应急车辆的预计到达时间，对二级子网进行抽取得到三级子网
    ss = []
    for i in range(len(edge_nodes1)):
        if edge_nodes1[i] != str(t):
            if nx.has_path(k, edge_nodes1[i], str(t)) == True:  # 查看i到t的路径是否存在
                cd = [p for p in nx.all_shortest_paths(k, source=edge_nodes1[i], target=str(t), weight='weight')]  # 最短路径
                #print(cd)
                for x in range(len(cd)):
                    cd[x].reverse()
                    # print(cd[x])
                    a = Travel_Distance
                    for y in range(len(cd[x])):
                        if y < len(cd[x]) - 1:
                            # print(k.get_edge_data(cd[x][y+1],cd[x][y]))
                            # print("边({},{})的长度:".format(str(cd[x][y+1]),str(cd[x][y])),k.get_edge_data(cd[x][y+1],cd[x][y]).get('weight'))
                            if k.get_edge_data(cd[x][y + 1], cd[x][y]).get('weight') < float(a):
                                ss.append(((cd[x][y + 1], cd[x][y]), k.get_edge_data(cd[x][y + 1], cd[x][y]).get('weight')))
                                a = float(a) - (k.get_edge_data(cd[x][y + 1], cd[x][y]).get('weight'))
                                # print('剩余长度：',a)
                            else:
                                ss.append(((cd[x][y + 1], cd[x][y]), a))
                                break
    # print(type(ss))
    # print(ss)

    # 删掉重复的路段
    res = []
    for i in ss:
        if i not in res:
            res.append(i)
    print(res)

    end = time.perf_counter()
    runtime = end - start
    m, s = divmod(runtime, 60)
    h, m = divmod(m, 60)
    print("运行时间:%02d:%02d:%02d" % (h, m, s))
    return res
'''
    plt.rcParams['figure.figsize'] = (20, 20)  # 单位是inches
    nx.draw(k
            , pos=pos_location
            #         , with_labels = True
            , node_size=500
    #        , with_labels=True
            , node_color='#7FFF00'
            # '#FF8000' #'#6DCAF2' # '#FF8000' # '#6DCAF2' #  '#B9F1E5'   #'grey'   # '#FFBFBF' #  'k' #nodes_col.values()   #'y'
            , width=0.5  # default = 1.0 , Line width of edges
            #         , font_size = 4
            #         , font_family = 'arial'
            , edge_color='grey'  # b, k, m, g,
            )
    #fig_name = 'result_figures/manhattan_map_dpi200.jpg'
    
    #plt.savefig(fig_name, dpi=200)
    #labels = nx.get_edge_attributes(Map, length)
    #nx.draw_networkx_edge_labels(Map, pos=pos_location, edge_labels = labels)
    plt.show()
'''
