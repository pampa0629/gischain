import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

class ArrowedEdge(FancyArrowPatch):
    def __init__(self, source, target, **kwargs):
        # 确定初始和结束点位置
        posA = source
        posB = target
        # 使用FancyArrowPatch来创建箭头
        super(ArrowedEdge, self).__init__(posA, posB, connectionstyle="arc3,rad=0.", **kwargs)

def draw_network_with_arrows(G, pos):
    # 对每条边使用自定义的箭头
    for edge in G.edges():
        source, target = edge
        arrow = ArrowedEdge(pos[source], pos[target], mutation_scale=20, arrowstyle='-|>', color="k", shrinkA=30, shrinkB=30)
        plt.gca().add_patch(arrow)
        # 此行确保箭头与图的边界不会被裁剪
        plt.plot()

import re, os

# 判断text是否是数值型
def is_numeric(text):
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return bool(re.match(pattern, text))

# 判断tool中，input 是否准备就绪; 就绪返回"ready",否则返回"noready"
# 如果是数值型、字符串类型，则直接OK；如果是文件型，则判断文件是否存在
def input_ready_status(key, value):
    if isinstance(value, (int, float)) or is_numeric(value) or os.path.isfile(value):
        return "ready"
    else:
        return "noready"

# 从tasks中构造图
def buildGaphic(G, tasks):
    # 添加任务和其输入输出到图中
    for task in tasks:
        task_name = task["name"]
        # task 节点增加status属性，包括以下状态：
        # todo  尚未处理，等到所有inputs都准备好后，就可以开始执行
        # ready inputs已经准备好，可以开始执行
        # doing 正在执行中
        # done  执行完毕
        G.add_node(task_name, color='green', type='task', status='todo')
        
        # data 节点增加status属性，包括以下状态：
        # noready  尚未准备好，等待上游task的输出
        # ready 已经准备好，可以为后续task使用
        inputs = task["inputs"]
        for key,value in inputs.items():
            status = input_ready_status(key, value)
            G.add_node(value, color='lightblue', type='data', status=status)
            # 对于 edge而言，区分input和output
            G.add_edge(value, task_name, type='input')
            
        output = task["output"]
        G.add_node(output, color='red', type='data', status='noready')
        G.add_edge(task_name, output, type='output')

# 从图中提取颜色映射
def get_color_mapping(G, tasks):
    # 创建颜色映射字典
    color_mapping = {
        "data": [],
        "task": [],
    }
    # 根据节点类型提取颜色
    for node in G.nodes():
        node_type = G.nodes[node]['type']
        color = G.nodes[node]['color']
        color_mapping[node_type].append(color)
    return color_mapping

# tasks 是一个List，里面的每个元素是一个字典，包括name、inputs和output三个key
def showdag(tasks):

    # 创建一个有向图
    G = nx.DiGraph()

    buildGaphic(G, tasks)
    color_mapping = get_color_mapping(G, tasks)
    
    plt.figure(figsize=(20,15))

    # 使用matplotlib进行绘图
    # seed 1 6 7 10
    pos = nx.spring_layout(G, k=0.5, iterations=200, seed=7, scale=2.0, center=(0, 0))

    # data_colors = [G.nodes[node]['color'] for node in G.nodes()]
    # 提取不同类型的节点
    data_nodes = [n for n, d in G.nodes(data=True) if d["type"]=="data"]
    task_nodes = [n for n, d in G.nodes(data=True) if d["type"]=="task"]

    # 使用不同的绘制函数为不同类型的节点绘制形状
    nx.draw_networkx_nodes(G, pos, nodelist=data_nodes, node_shape="o",
                        node_color=color_mapping["data"], node_size=3000)  # 圆形表示data
    nx.draw_networkx_nodes(G, pos, nodelist=task_nodes, node_shape="h",
                        node_color=color_mapping["task"], node_size=3000)  # 矩形表示task

    nx.draw_networkx_labels(G, pos)
    # 定义箭头样式
    draw_network_with_arrows(G, pos)

    # plt.title('DAG depicting tasks and their inputs/outputs')
    plt.show()
    