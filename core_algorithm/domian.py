# author: Weiqi Yu
# 开发时间: 2022/10/20 16:17
import xml.dom.minidom
# dom = xml.dom.minidom.parse('map_data/interpreter_beijing')
# dom = xml.dom.minidom.parse('map_data/interpreter_shenzhen')
# dom = xml.dom.minidom.parse('map_data/interpreter_shanghai')
# dom = xml.dom.minidom.parse('map_data/interpreter_guangzhou')
# dom = xml.dom.minidom.parse('map_data/interpreter_hangzhou')
# dom = xml.dom.minidom.parse('map_data/interpreter_chengdu')
dom = xml.dom.minidom.parse('C:/Users/ywq/Desktop/sumo/manhattan/map.osm')

root = dom.documentElement
#root
print(root.nodeName)
print(root.nodeValue)
print(root.nodeType)
print(root.ELEMENT_NODE)