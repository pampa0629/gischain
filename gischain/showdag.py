import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import io
from . import base

# 得到G的行列数
def get_row_col(G):
    node_positions = {}
    for node in G.nodes():
        pos = G.get_node(node).attr['pos']
        node_positions[node] = tuple(map(float, pos.split(',')))

    # Calculate the maximum rows and columns
    max_row = max(pos[0] for pos in node_positions.values()) + 1
    max_col = max(pos[1] for pos in node_positions.values()) + 1
    return max_row, max_col

# 设置G的方向
def set_direction(G):
    row, col = get_row_col(G)
    # direction = 'LR' # 默认为左右
    # 如果行数大于列数的2倍，或者列数大于500，则设置为上下
    # if col / row > 2 or col > 500:
    direction = 'TB' # 上下更好看
    G.graph_attr.update(rankdir=direction) # TB：上下；LR：左右
    # print("direction:", direction)

# 按照一定频率刷新页面
def refresh(frame, G, pos, shares):
    # 把shares中的颜色，设置给G中对应的节点
    for node in G.nodes():
        node_name = node.get_name()
        node.attr['fillcolor'] = shares[node_name]['color']
        # 如果任务节点的状态为doing，则通过修改节点的颜色，实现闪烁效果
        if shares[node_name]['type'] == 'task' and shares[node_name]['status'] == 'doing' and frame % 2 == 1:
            node.attr['fillcolor'] = "white"

    # 重新绘制图形
    image_data = G.draw(format='png', prog='dot')
    image = Image.open(io.BytesIO(image_data))
    plt.imshow(image)
    plt.title(shares['title'])

# 用shares还原DAG，并动态绘制
def show(shares):
    # 通过shares来创建DAG
    G = base.resotreDAG(shares)

    fig = plt.figure(figsize=(8,12))
    # 关闭横轴和纵轴
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    from matplotlib import rcParams
    # 设置中文字体为默认字体
    plt.rcParams['font.family'] = 'Arial Unicode MS'
    
    pos = G.layout(prog='fdp') # neato dot fdp
    G.node_attr['style'] = 'filled'  # 设置节点样式为填充
    set_direction(G) # 自动设置合理的方向
    
    anim = FuncAnimation(fig, refresh, fargs=(G,pos, shares,), frames=range(100), repeat=True, interval=100)
    plt.show()