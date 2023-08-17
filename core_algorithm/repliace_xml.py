# author: Weiqi Yu
# 开发时间: 2023/8/12 8:30
# -*- coding:utf-8 -*-

# import glob
#
# xmls = glob.glob('D:/experiment/sumo/test1/net/compliance/new/fcd_ohi.out.xml')
# for one_xml in xmls:
#     print(one_xml)
#     f = open(one_xml, 'r+', encoding='utf-8')
#     all_the_lines = f.readlines()
#     f.seek(0)
#     f.truncate()
#     for line in all_the_lines:
#         line = line.replace('d1', 'Our approach')
#         #line = line.replace('cat', 'bike')
#         f.write(line)
#     f.close()
import re  # 自定义正则


# 自定义正则
rex = 'd1'
new_str = 'Our appraoch'
old_file_path = r'D:/experiment/sumo/test1/net/compliance/new/fcd_ohi.out.xml'
new_file_path = r'D:/experiment/sumo/test1/net/compliance/new/ohi.xml'


def match_timestamp(repex, eachline):
    p = re.compile(repex)
    return p.findall(eachline)


# 打开旧文件，将每一行yield后作为迭代器返回。
def old_file_yield(old_file_path):
    with open(old_file_path, 'r') as  oldf:
        while True:
            line = oldf.readline()
            yield line
            if not line:
                oldf.close()
                break


# 打开新文件开始逐行读取替换。
def replace_match(old_file_path, new_file_path):
    count = 0
    with open(new_file_path, "w") as newf:
        for line in old_file_yield(old_file_path):
            ifmatch = match_timestamp(rex, line)
            if not line:
                newf.close()
                return count
                break
            elif ifmatch != []:
                count += 1
                print("替换前：%s" % line)
                line = line.replace(rex, new_str)
                print("替换后：%s" % line)
                newf.write(line)
            else:
                newf.write(line)


print('一共替换了%s行' % replace_match(old_file_path, new_file_path))