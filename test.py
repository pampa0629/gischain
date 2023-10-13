import os

file_path = "example.txt"
if os.path.isfile(file_path):
    print(f"路径 '{file_path}' 指向一个文件")
else:
    print(f"路径 '{file_path}' 不是一个文件或不存在")
