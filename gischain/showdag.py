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

import os

# 按照一定频率刷新页面
def refresh(frame, G, pos, shares):
    # 提取不同类型的节点
    data_nodes = [node for node in G.nodes if shares.get(node, {}).get('type') == "data"]
    data_colors = [shares[node]['color'] for node in G.nodes if shares.get(node, {}).get('type') == "data"]

    task_nodes = [node for node in G.nodes if shares.get(node, {}).get('type') == "task"]
    task_colors = [shares[node]['color'] for node in G.nodes if shares.get(node, {}).get('type') == "task"]
    
    # 使用不同的绘制函数为不同类型的节点绘制形状
    nx.draw_networkx_nodes(G, pos, nodelist=data_nodes, node_shape="o",
                        node_color=data_colors, node_size=2000)  # 圆形表示data
    nx.draw_networkx_nodes(G, pos, nodelist=task_nodes, node_shape="h",
                        node_color=task_colors, node_size=4000)  # 六边形表示task

    node_labels = {node: os.path.basename(str(G.nodes[node]["lable"])) for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # 定义箭头样式
    draw_network_with_arrows(G, pos)


from matplotlib.animation import FuncAnimation

def showdag(G, shares):
    fig = plt.figure(figsize=(20,15))
    # 使用matplotlib进行绘图
    # seed 1 6 7 10
    pos = nx.spring_layout(G, k=0.5, iterations=200, seed=7, scale=2.0, center=(0, 0))
    refresh(None, G, pos, shares)
    anim = FuncAnimation(fig, refresh, fargs=(G,pos, shares,), frames=100, repeat=False, interval=1000)
    plt.show()
    