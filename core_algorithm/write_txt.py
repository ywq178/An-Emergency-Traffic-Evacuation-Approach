# author: Weiqi Yu
# 开发时间: 2023/7/28 10:25
file_path = "D:\pythonProject/O-YN-91.txt"
with open(file_path, "r+") as file:
    lines = file.readlines()

    line_number = 0
    new_content = "1"

    lines[line_number] = new_content + "\n"

    # 将修改后的内容写回文件
    file.seek(0)  # 将文件指针定位到文件开头
    file.writelines(lines)
