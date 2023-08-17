# author: Weiqi Yu
# 开发时间: 2022/10/22 15:52
"下载的文件（.parquet）转化为文件(.csv)"
import pandas as pd
#加载文件
data = pd.read_parquet(r"C:\Users\ywq\Downloads\yellow_tripdata_2010-01.parquet")
#以csv文件保存
data.to_csv(r'C:\Users\ywq\Downloads\data4.csv')
