# author: Weiqi Yu
# 开发时间: 2022/12/10 21:57
"作用：将车辆文件（rou.xml）的车辆信息按出发时间从小到大进行重新排序"
import xml.etree.ElementTree as ET

tree = ET.ElementTree(file=r"D:\pythonProject\mix_veh.rou.xml")  #输入rou.xml文件
root = tree.getroot()
for child in root:
    print(child.tag,child.get('depart'),type(child.get('depart')))

root[:] = sorted(root, key=lambda child: (child.tag,float(child.get('depart')))) #按照depart进行排序

tree.write("vehicle.rou.xml")   #输出排好序的rou.xml文件


