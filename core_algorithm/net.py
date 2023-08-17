# author: Weiqi Yu
# 开发时间: 2022/12/1 15:31
import sumolib
sumo_net = sumolib.net.readNet('C:\\Users\\ywq\\Desktop\\sumo\\test1\\net\\no.net.xml')
Net_edge = sumo_net.getEdges()  # 访问路网中的edge
# print(Net_edge,type(Net_edge),len(Net_edge))
Net_edgeID = []  # 储存路网的所有edge的ID，ID表示
for i in range(len(Net_edge)):
    Net_edgeID.append(Net_edge[i].getID())
# print(Net_edgeID)
a=sumo_net.getNeighboringEdges(8292.1,17603.46)
print(a)