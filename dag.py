import networkx as nx
import matplotlib.pyplot as plt

# 创建一个有向图
G = nx.DiGraph()

# 定义任务列表，每个任务是一个元组 (任务名, 输入列表, 输出列表)
tasks = [
    ("TaskA", [], ["Data1"]),
    ("TaskB", ["Data1"], ["Data2"]),
    ("TaskC", ["Data1"], ["Data3"]),
    ("TaskD", ["Data2", "Data3"], ["Data4"]),
    ("TaskE", ["Data4"], ["Result"])
]

# 添加任务节点到图中
for task in tasks:
    task_name, inputs, outputs = task
    G.add_node(task_name, inputs=inputs, outputs=outputs)

# 添加有向边表示输入到输出的关系
for task in tasks:
    task_name, inputs, _ = task
    for input_task in inputs:
        G.add_edge(input_task, task_name)

# 绘制DAG图
pos = nx.spring_layout(G, seed=42)  # 定义节点的布局
nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=10, font_weight="bold")
plt.title("DAG图")
plt.show()
