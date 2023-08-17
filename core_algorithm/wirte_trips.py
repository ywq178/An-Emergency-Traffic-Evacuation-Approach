# author: Weiqi Yu
# 开发时间: 2022/12/2 11:52
"作用：读取网上下载的车辆信息文件（.csv）提前有用信息（id，出发时间，出发和到达经纬度）"
"duarouter --trip-files C:\Users\ywq\Desktop\config2.trips.xml --net-file C:\Users\ywq\Desktop\sumo\test1\net\no.net.xml --output-file result1.rou.xml --mapmatch.distance 1000000000000000000000 --ignore-errors"
from xml.dom.minidom import Document
import pandas as pd


doc = Document()  #创建DOM文档对象
item = doc.createElement('routes') #创建根元素
doc.appendChild(item)


data = pd.read_csv(r'C:\Users\ywq\Desktop\taxi_data.csv')
print(data.shape)
print(data.shape[0])
for i in range(data.shape[0]):
    #if data['pickup_longitude'][i] <= -74.0327 or data['pickup_longitude'][i] >= -73.9078 or data['dropoff_longitude'][i] <= -74.0327 or data['dropoff_longitude'][i] >= -73.9078 or data['pickup_latitude'][i] >= 40.8815 or data['pickup_latitude'][i] <= 40.6960 or data['dropoff_latitude'][i] >= 40.8815 or data['dropoff_latitude'][i] <= 40.6960:
    #    break
    #else:
    #print(data['pickup_longitude'][i],data['pickup_latitude'][i],data['dropoff_longitude'][i],data['dropoff_latitude'][i])
    time = (int(data['pickup_datetime'][i][-2:]))*60 + (int(data['pickup_datetime'][i][-5:-3]))*3600
    print(data['pickup_datetime'][i],type(data['pickup_datetime'][i]),time)
    #print(int(data['pickup_datetime'][i][-2:]))
    #print(data['pickup_datetime'][i][-5:-3])

    veh = doc.createElement('trip')
    item.appendChild(veh)
    veh.setAttribute('id', "{}".format(i+14000))
    veh.setAttribute('depart',"{}".format(time))
    veh.setAttribute('fromLonLat',"{},{}".format(data['pickup_longitude'][i],data['pickup_latitude'][i]))
    veh.setAttribute('toLonLat', "{},{}".format(data['dropoff_longitude'][i],data['dropoff_latitude'][i]))
    item.appendChild(veh)

f = open(r'C:\Users\ywq\Desktop\config2.trips.xml','w')
#f.write(doc.toprettyxml(indent = '\t', newl = '\n', encoding = 'utf-8'))
doc.writexml(f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
f.close()


