# author: Weiqi Yu
# 开发时间: 2023/7/24 18:22

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 09:15:33 2022
时间间隔+距离
@author: ywq
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random_0
import random
import traci
import time
import sumolib
from sumolib import checkBinary
import numpy as np
import math
#import real_net
import Reroute
#import RVs_shortpath
import jj
import linecache

# 检测是否已经添加环境变量
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# sumo自带的，不知道有啥用
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# 主函数
if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumocfgfile = "D:\\experiment\\sumo\\test1\\net\\compliance\\map.sumocfg"  # sumocfg文件的位置
    traci.start([sumoBinary, "-c", sumocfgfile])  # 打开sumocfg文件

    sumo_net = sumolib.net.readNet('D:\\experiment\\sumo\\test1\\net\\no_htcc.net.xml')  # 访问路网文件
    Net_edge = sumo_net.getEdges()  # 访问路网中的edge
    # print(Net_edge,type(Net_edge),len(Net_edge))
    Net_edgeID = []  # 储存路网的所有edge的ID，ID表示
    for i in range(len(Net_edge)):
        Net_edgeID.append(Net_edge[i].getID())
    # print(Net_edgeID)
    EV_Position = 0
    #start = time.perf_counter()
    ParkingAreaList = traci.parkingarea.getIDList()
    juice=[]
    start = time.perf_counter()

    for step in range(0, 7200000000000):  # 仿真时间
        traci.simulationStep()  # 一步一步（一帧一帧）进行仿真
        # time.sleep(0.1)
        simulation_time = traci.simulation.getTime()  # 获得仿真时间
        print("仿真时间是", simulation_time)
        all_vehicle_id = traci.vehicle.getIDList()  # 获得所有车的id
        # 获取所有车的position
        all_vehicle_position = [(i, traci.vehicle.getPosition(i)) for i in all_vehicle_id]

        # a=networkx_manhattan.Grap(44,43,100) #测试二级子网的提取
        # print(a)
        Three_network = []  # 储存三级子网

        for i in range(len(all_vehicle_id)):
            if all_vehicle_id[i] == 'd1':
                EV_Route = traci.vehicle.getRoute('d1')  # 急救车的路线(路段edge组成)
                print(EV_Route)
                EV_current_edgeID = traci.vehicle.getRoadID('d1')  # EV当前所在edge
                # print(EV_current_edgeID)
                if step % 10 == 0:  # 每五秒执行一次
                 for r in range(len(EV_Route)):  # 应急车辆的当前位置
                    if EV_current_edgeID == EV_Route[r]:
                        # print(r)
                        EV_failRoute=[] #未通过路段用ID表示
                        EV_Route_networkx = []  # 储存未通过应急车辆路线的边,（）表示
                        time1 = 0
                        for f in range(r+1, len(EV_Route)):  # 统计EV还未通过edge（包括当前所在的路段）
                            single_edge = sumo_net.getEdge(EV_Route[f])
                            FromNode_EV = single_edge.getFromNode().getID()
                            ToNode_EV = single_edge.getToNode().getID()
                            #print(FromNode_EV,ToNode_EV)
                            EV_Route_networkx.append((FromNode_EV, ToNode_EV))
                            EV_failRoute.append(EV_Route[f])
                            if traci.vehicle.getDrivingDistance('d1', EV_Route[f], 0)<300:
                                    time1=time1+1
                                   # if EV_Route[f] not in juice:
                                   #     juice.append(EV_Route[f])
                                    S=traci.vehicle.getDrivingDistance('d1', EV_Route[f], 0)
                                    #    S = math.ceil((-B + math.sqrt(D)) / (2 * A))
                                        # print(S)  #求出当前EV到路线上各十字路口的预计时间
                                    travel_distance = S+(5*time1* 13.89)
                                    single_edge = sumo_net.getEdge(EV_Route[f])
                                    FromNode = single_edge.getFromNode().getID()
                                    ToNode = single_edge.getToNode().getID()
                                    # print(FromNode,ToNode)
                                    # print(networkx_manhattan.Grap(int(FromNode),int(ToNode),travel_distance))
                                    #a = real_net.Grap(FromNode, ToNode,int(travel_distance))  # 输出EV还未通过的若干路段的子网
                                    print(FromNode, ToNode, int(travel_distance))
                                    a = jj.Grap(FromNode, ToNode, int(travel_distance))
                                    if Three_network == []:  # 如果为空，储存第一个未通过路段的子网
                                        Three_network = a
                                    else:  # 否则，a与Three_network取并集！！！将EV未通过路段的所有子网取并集
                                        for l in range(len(a)):
                                            bb = 0
                                            for k in range(len(Three_network)):
                                                if a[l][0] == Three_network[k][0] and a[l][1] > Three_network[k][1]:  # 相同路段下，如果a的疏散道路长度大于Three_network中的
                                                    Three_network.remove(Three_network[k])  # 删除原本的
                                                    Three_network.append(a[l])  # 加入新的
                                                if a[l][0] == Three_network[k][0]:
                                                    bb = bb + 1
                                            if bb == 0:  # 如果a中的路段在Three_network中没有
                                                Three_network.append(a[l])  # 直接加入到Three_network
                            #print(Three_network)

                        if len(Three_network) > 0: #子网上的车辆
                            print(Three_network)
                            for t in range(len(Three_network)):  # for循环三级子网
                                for u in range(len(Net_edgeID)):  # for循环路网的edge
                                    edge_inf = sumo_net.getEdge(Net_edgeID[u])  # 获得Net_edgeID[u]的基本信息
                                    From_Node = edge_inf.getFromNode().getID()  # 它的from节点（入节点）
                                    To_Node = edge_inf.getToNode().getID()  # 它的to节点（出节点）
                                    Length = edge_inf.getLength()  # 它的长度
                                    if Three_network[t][0][0] == From_Node and Three_network[t][0][1] == To_Node:  # 找到三级子网疏散路段的对应路段ID
                                        n = traci.edge.getLastStepVehicleIDs(Net_edgeID[u])  # 获取路段的车辆ID集合
                                        print(Three_network[t], Net_edgeID[u])  # 疏散道路信息，第一个用（）,第二个用ID
                                        for p in range(len(n)):
                                            if n[p] != 'd1':

                                             with open('juice19.txt', 'r') as file:
                                                 # 读取文件的所有行
                                                 lines = file.readlines()
                                                 # 获取特定行的数据
                                                 specific_line = lines[int(n[p])]  # 假设我们需要获取第4行的数据
                                             #text = linecache.getline('juice37.txt', int(n[p]))

                                             # #print(text,type(text),n[p])
                                             if int(specific_line) == 1:
                                                #print(1234567)
                                                m = Length - traci.vehicle.getLanePosition(n[p])
                                                if m < Three_network[t][1]:
                                                    route = traci.vehicle.getRoute(n[p])
                                                    RoadID_RV = traci.vehicle.getRoadID(n[p])#RV当前位置
                                                    pos=route.index(RoadID_RV)
                                                    #print(pos)
                                                    for e in range(pos,len(route)): #RV未通过的路线
                                                        if route[e] in EV_failRoute: #判断疏散路段上的车辆是否经过应急路线
                                                            print(m, n[p], route, RoadID_RV,route[e])
                                                            Des_edgeID_RV = sumo_net.getEdge(route[-1])
                                                            To_Node_RV = Des_edgeID_RV.getToNode().getID()
                                                            Sou_edgeID_RV = sumo_net.getEdge(RoadID_RV)
                                                            From_Node_RV = Sou_edgeID_RV.getToNode().getID()
                                                            # print(int(From_Node_RV),int(To_Node_RV))
                                                            h = Reroute.Grap(From_Node_RV, To_Node_RV,EV_Route_networkx)  # 返回一条最短路径
                                                            g = []  # 储存RV的重新路线
                                                            g.append(RoadID_RV)  # 先存入RV当前所在的edge
                                                            for s in range(len(h) - 1):  # 返回的路线，（）表示
                                                                for q in range(len(Net_edgeID)):  # 路网中edge，ID表示
                                                                    RV_edge = sumo_net.getEdge(Net_edgeID[q])
                                                                    FromRV = RV_edge.getFromNode().getID()
                                                                    ToRV = RV_edge.getToNode().getID()
                                                                    if h[s] == FromRV and h[s + 1] == ToRV:  # 找到（）对应的ID
                                                                        g.append(Net_edgeID[q])
                                                            print(g)
                                                            traci.vehicle.setRoute(n[p],g)  # 重新规划路线

                                                            # file_path = "D:\pythonProject/O-YN-19.txt"
                                                            # with open(file_path, "r+") as file:
                                                            #     lines = file.readlines()
                                                            #     line_number = int(n[p])  # 替换为你需要替换的行号（从0开始计数）
                                                            #     new_content = "1"
                                                            #     lines[line_number] = new_content + "\n"
                                                            #     # 将修改后的内容写回文件
                                                            #     file.seek(0)  # 将文件指针定位到文件开头
                                                            #     file.writelines(lines)

                                                            break

                if EV_current_edgeID in Net_edgeID:
                        if traci.parkingarea.getVehicleCount('accident_point1') == 0:
                                single_edge = sumo_net.getEdge(EV_current_edgeID)
                                FromNode = single_edge.getFromNode().getID()
                                ToNode = single_edge.getToNode().getID()
                                LaneID = single_edge.getLanes()
                                h = []
                                # print(LaneID,type(LaneID))
                                for o in range(len(LaneID)):
                                    h.append(LaneID[o].getID())
                                # print(h)

                                # 同一车道的前程RVs变道给应急车辆绕道
                                q1 = traci.vehicle.getLaneID('d1')  # 获得救护车所在车道
                                # print(q1)
                                h.remove(q1)
                                q2 = traci.lane.getLastStepVehicleIDs(q1)  # 获得车道的车辆ID
                                q3 = traci.vehicle.getLanePosition('d1')  # 获得救护车位置
                                # print(h)
                                for w in q2:
                                     if w != 'd1':
                                      #text1 = linecache.getline('juice82.txt', int(w))
                                      # with open('juice10.txt', 'r') as file:
                                      #     # 读取文件的所有行
                                      #     lines = file.readlines()
                                      #     # 获取特定行的数据
                                      #     specific_line = lines[int(w)]  # 假设我们需要获取第4行的数据
                                      # if int(specific_line) == 1:
                                        c = traci.vehicle.getLanePosition(w)
                                        if c > q3 and len(h) >= 1:
                                            traci.vehicle.changeLane(w, random.choice(h)[-1], 3)
                                        if c > q3 and len(h) == 0:
                                            for j in range(len(ParkingAreaList)):
                                                parking_area = traci.parkingarea.getLaneID(ParkingAreaList[j])
                                                if parking_area == q1:
                                                    traci.vehicle.setParkingAreaStop(w, ParkingAreaList[j], duration=10)

        if len(all_vehicle_id)==0:
             traci.close()
