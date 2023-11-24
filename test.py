import pygraphviz as pgv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 创建一个简单的图形
G = pgv.AGraph(strict=False)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)

# 初始化图形
# pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
G.layout(prog='dot')
nodes = G.nodes()

# 要闪烁的节点
blink_node = "2"

# 设置初始可见性
visible = {node: True for node in G.nodes()}
print(visible)
# 创建绘图对象
fig, ax = plt.subplots()
G.node_attr['style'] = 'filled'  # 设置节点样式为填充


def update(frame, visible,blink_node):
    print("frame:", frame)
    # 切换节点的可见性
    # visible[blink_node] = not visible[blink_node]
    # print(visible)
    # print(blink_node)
    # print(visible[blink_node])
    visible[blink_node] = False if visible[blink_node] else True

    if visible[blink_node]:
        G.get_node(blink_node).attr.update(fillcolor='lightblue')  # 修改节点的颜色
    else:
        G.get_node(blink_node).attr.update(fillcolor='white')  # 还原节点颜色
    
    
    # 更新节点的可见性
    ax.clear()
    G.draw(format='png', prog='dot', path='temp.png')
    img = plt.imread('temp.png')
    ax.imshow(img)
    ax.axis('off')

# 创建动画
ani = FuncAnimation(fig, update, fargs=(visible,blink_node,), frames=range(100), repeat=True, interval=500)

plt.show()
