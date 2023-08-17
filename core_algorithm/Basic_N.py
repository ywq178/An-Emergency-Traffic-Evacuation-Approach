# author: Weiqi Yu
# 开发时间: 2023/7/24 21:25

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
    #sumo_connection = sumolib.net.Connection('C:\\Users\\ywq\\Desktop\\sumo\\test1\\net\\no.net.xml') #交叉口
    #Net_connection = sumo_connection.getTLSID()

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

    for step in range(0, 720000000):  # 仿真时间
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


        if len(all_vehicle_id) == 0:
             traci.close()
        # if step > 600:
        #     if len(all_vehicle_id) == 0:
        #         traci.close()

