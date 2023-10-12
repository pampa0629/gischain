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

# tasks 是一个List，里面的每个元素是一个字典，包括name、inputs和output三个key
def showdag(tasks):

    # 创建一个有向图
    G = nx.DiGraph()

    # 添加任务和其输入输出到图中
    for task in tasks:
        task_name = task["name"]
        # print(task_name)
        G.add_node(task_name, color='green', type='task')
        
        inputs = task["inputs"]
        for key,value in inputs.items():
            # print(value)
            G.add_node(value, color='lightblue', type='data')
            G.add_edge(value, task_name)
            
        output = task["output"]
        # print(output)
        G.add_node(output, color='red', type='data')
        G.add_edge(task_name, output)

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

    plt.figure(figsize=(20,15))

    # 使用matplotlib进行绘图
    pos = nx.spring_layout(G, k=1.0, iterations=100, seed=42, scale=2.0, center=(0, 0))

    # data_colors = [G.nodes[node]['color'] for node in G.nodes()]
    # 提取不同类型的节点
    data_nodes = [n for n, d in G.nodes(data=True) if d["type"]=="data"]
    task_nodes = [n for n, d in G.nodes(data=True) if d["type"]=="task"]

    # 使用不同的绘制函数为不同类型的节点绘制形状
    nx.draw_networkx_nodes(G, pos, nodelist=data_nodes, node_shape="o",
                        node_color=color_mapping["data"], node_size=2000)  # 圆形表示data
    nx.draw_networkx_nodes(G, pos, nodelist=task_nodes, node_shape="h",
                        node_color=color_mapping["task"], node_size=2000)  # 矩形表示task

    nx.draw_networkx_labels(G, pos)
    # 定义箭头样式
    draw_network_with_arrows(G, pos)

    plt.title('DAG depicting tasks and their inputs/outputs')
    plt.show()
    