import networkx as nx
import matplotlib.pyplot as plt

# 假设我们有以下任务和它们的输入输出关系
tasks = [
    {"id": "task1", "input": [], "output": ["A"]},
    {"id": "task2", "input": ["A"], "output": ["B"]},
    {"id": "task3", "input": ["B"], "output": ["C", "D"]},
    {"id": "task4", "input": ["D"], "output": ["E"]},
]

# 创建一个有向图
G = nx.DiGraph()

# 添加任务和其输入输出到图中
for task in tasks:
    task_id = task["id"]
    G.add_node(task_id, color='lightblue', type='task')
    
    for inp in task["input"]:
        G.add_node(inp, color='green', type='data')
        G.add_edge(inp, task_id)

    for out in task["output"]:
        G.add_node(out, color='red', type='data')
        G.add_edge(task_id, out)

# 使用matplotlib进行绘图
pos = nx.spring_layout(G)
colors = [G.nodes[node]['color'] for node in G.nodes()]

plt.figure(figsize=(10,6))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=3000, edge_color='gray', width=1.5)
plt.title('DAG depicting tasks and their inputs/outputs')
plt.show()
