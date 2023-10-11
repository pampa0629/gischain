import networkx as nx
import matplotlib.pyplot as plt

text = """
[
    {
        "name": "buffer",
        "inputs": {
            "datafile": "data/railway.shp",
            "radius": 500
        },
        "output": "data/railway_buffer.shp"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/railway_buffer.shp",
            "datafile2": "data/land.shp"
        },
        "output": "data/buffer_land.shp"
    },
    {
        "name": "slope",
        "inputs": {
            "tifffile": "data/terrain.tif"
        },
        "output": "data/slope.tif"
    },
    {
        "name": "extractByValues",
        "inputs": {
            "tifffile": "data/slope.tif",
            "min": 0,
            "max": 10
        },
        "output": "data/slope_10.tif"
    },
    {
        "name": "polygon2mask",
        "inputs": {
            "shpfile": "data/buffer_land.shp",
            "tiffile": "data/terrain.tif"
        },
        "output": "data/buffer_land_mask.tif"
    },
    {
        "name": "rasterOverlay",
        "inputs": {
            "datafile1": "data/slope_10.tif",
            "datafile2": "data/buffer_land_mask.tif"
        },
        "output": "data/slope_land.tif"
    },
    {
        "name": "calculateArea",
        "inputs": {
            "datafile": "data/slope_land.tif"
        },
        "output": "data/area_result"
    }
]
"""

# 假设我们有以下任务和它们的输入输出关系
# tasks = [
#     {"id": "task1", "input": [], "output": ["A"]},
#     {"id": "task2", "input": ["A"], "output": ["B"]},
#     {"id": "task3", "input": ["B"], "output": ["C", "D"]},
#     {"id": "task4", "input": ["D"], "output": ["E"]},
# ]

import json
tasks = json.loads(text)
# for task in tasks:
#     print(task["name"])
#     print(task["inputs"])
#     print(task["output"])

# 创建一个有向图
G = nx.DiGraph()

# 添加任务和其输入输出到图中
for task in tasks:
    task_name = task["name"]
    print(task_name)
    G.add_node(task_name, color='green', type='task')
    
    inputs = task["inputs"]
    for key,value in inputs.items():
        print(value)
        G.add_node(value, color='lightblue', type='data')
        G.add_edge(value, task_name)
        
    output = task["output"]
    print(output)
    G.add_node(output, color='red', type='data')
    G.add_edge(task_name, output)

# 使用matplotlib进行绘图
pos = nx.spring_layout(G)
colors = [G.nodes[node]['color'] for node in G.nodes()]

plt.figure(figsize=(10,6))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, edge_color='gray', width=1.5)
plt.title('DAG depicting tasks and their inputs/outputs')
plt.show()
