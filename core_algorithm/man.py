# author: Weiqi Yu
# 开发时间: 2022/9/30 11:19
import xml.dom.minidom
#读取xml文档
# dom = xml.dom.minidom.parse('map_data/interpreter_beijing')
# dom = xml.dom.minidom.parse('map_data/interpreter_shenzhen')
# dom = xml.dom.minidom.parse('map_data/interpreter_shanghai')
# dom = xml.dom.minidom.parse('map_data/interpreter_guangzhou')
# dom = xml.dom.minidom.parse('map_data/interpreter_hangzhou')
# dom = xml.dom.minidom.parse('map_data/interpreter_chengdu')
#dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\test1\new.net.xml')
#dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\manhattan\st.osm')
#dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\ny.net.xml')
#dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\test1\net\real_net.net.xml')
dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\test1\net\no_htcc.net.xml')
#dom = xml.dom.minidom.parse(r'C:\Users\ywq\Desktop\sumo\test1\net\test.net.xml')
root = dom.documentElement
root
print(root.nodeName)
print(root.nodeValue)
print(root.nodeType)
print(root.ELEMENT_NODE)
