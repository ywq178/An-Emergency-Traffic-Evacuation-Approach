# author: Weiqi Yu
# 开发时间: 2022/9/30 11:23
import networkx as nx
import matplotlib.pyplot as plt
import copy
import man

# 构建有向图对象
Map = nx.DiGraph()

node = man.root.getElementsByTagName('node') # 根据标签获取 xml 节点对象集合
print(node[0].nodeName)

pos_location = {}  # position of all nodes in the graph" to draw the figure
loc = []
for i in range(len(node)):
    ID = node[i].getAttribute('id')
    lat = float(node[i].getAttribute('lat'))
    lon = float(node[i].getAttribute('lon'))
    #     print(ID, lat, lon)

    Map.add_node(ID
                 , ID=ID
                 , lat=lat
                 , lon=lon
                 )
    pos_location[ID] = (lon, lat)
    loc.append([lon, lat])

way_set = man.root.getElementsByTagName('way')
# print(way_set[0].nodeName)

for way in way_set:
    previous_node = start_node_id = way.getElementsByTagName('nd')[0].getAttribute('ref')
    end_node_id = way.getElementsByTagName('nd')[-1].getAttribute('ref')

    for sub_node in way.getElementsByTagName('nd'):
        current_node_id = sub_node.getAttribute('ref')
        if (current_node_id != start_node_id):
            Map.add_edge(previous_node, current_node_id
                         , way_type=0
                         )
            previous_node = current_node_id
#     print(sub_node.getAttribute('ref'))

G2 = copy.deepcopy(Map)
for node in Map.nodes:
    if ((Map.nodes[node]['lat'] >= 40.8815 or Map.nodes[node]['lat'] <= 40.6960) and node in G2.nodes):
        G2.remove_node(node)
    if ((Map.nodes[node]['lon'] <= -74.0327 or Map.nodes[node]['lon'] >= -73.9078) and node in G2.nodes):
        G2.remove_node(node)

G3 = nx.to_undirected(G2)

plt.rcParams['figure.figsize'] = (20, 20)  # 单位是inches
nx.draw(G3
        , pos=pos_location
        #         , with_labels = True
        , node_size=0.0001
        , node_color='grey'
        # '#FF8000' #'#6DCAF2' # '#FF8000' # '#6DCAF2' #  '#B9F1E5'   #'grey'   # '#FFBFBF' #  'k' #nodes_col.values()   #'y'
        , width=0.5  # default = 1.0 , Line width of edges
        #         , font_size = 4
        #         , font_family = 'arial'
        , edge_color='grey'  # b, k, m, g,
        )
#fig_name = 'result_figures/manhattan_map_dpi200.jpg'

#plt.savefig(fig_name, dpi=200)
plt.show()