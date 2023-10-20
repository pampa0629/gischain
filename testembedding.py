
from tools import buffer, define, overlay,calculateArea,slope,extractByMask,extractByValues,rasterOverlay,polygon2mask
input = "修一条铁路，宽度为50米，需要计算占用周边耕地的面积。"
# buffer = "王后"
# other = "地球"

import testgptem
import numpy as np


# 计算余弦相似度
def cos_simily(data1, data2):
    result = np.dot(data1, data2) / (np.linalg.norm(data1) * np.linalg.norm(data2))
    return result
# print("计算余弦相似度")

# print(input_buffer)

# input_other = np.dot(input, other) / (np.linalg.norm(input) * np.linalg.norm(other))
# print(input_other)


# 计算欧几里德距离
def ou_simily(data1, data2):
    result = np.linalg.norm(data1 - data2)
    return result
# print("计算欧几里德距离")
# input_buffer = np.linalg.norm(input - buffer)
# print(input_buffer)
# input_other = np.linalg.norm(input - other)
# print(input_other)

def man_simily(data1, data2):
    result = np.sum(np.abs(data1 - data2))
    return result
# 计算曼哈顿距离
# print("计算曼哈顿距离")
# input_buffer = np.sum(np.abs(input - buffer))
# print(input_buffer)

# input_other = np.sum(np.abs(input - other))
# print(input_other)

input = testgptem.text2em(input)
# buffer = testgptem.text2em(buffer)
# other = testgptem.text2em(other)

tools = define.get_tools_name()
# discs = [(tool,define.get_tool_disc(tool),testgptem.text2em(define.get_tool_disc(tool))) for tool in tools]
discs = [(tool,define.get_tool_disc(tool),testgptem.text2em(define.get_tool_disc(tool))) for tool in tools]

for tool,disc,emb in discs:
    simily = cos_simily(input, emb)
    print(f"{tool} :{simily}")

print("====================================================")
for tool,disc,emb in discs:
    simily = ou_simily(input, emb)
    print(f"{tool} :{simily}")

print("====================================================")
for tool,disc,emb in discs:
    simily = man_simily(input, emb)
    print(f"{tool} :{simily}")

