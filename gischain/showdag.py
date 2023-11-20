import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import io
from . import base

# 按照一定频率刷新页面
def refresh(frame, G, pos, shares):
    # 把shares中的颜色，设置给G中对应的节点
    for node in G.nodes():
        node_name = node.get_name()
        node.attr['fillcolor'] = shares[node_name]['color']
    image_data = G.draw(format='png', prog='dot')
    image = Image.open(io.BytesIO(image_data))
    plt.imshow(image)
    plt.title(shares['title'])
    
def showdag(shares):
    # 通过shares来创建DAG
    G = base.resotreDAG(shares)

    fig = plt.figure(figsize=(16,12))
    # 关闭横轴和纵轴
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    from matplotlib import rcParams
    # 设置中文字体为默认字体
    plt.rcParams['font.family'] = 'Arial Unicode MS'
    
    pos = G.layout(prog='dot')
    G.node_attr['style'] = 'filled'  # 设置节点样式为填充
    
    refresh(None, G, pos, shares)
    anim = FuncAnimation(fig, refresh, fargs=(G,pos, shares,), frames=100, repeat=True, interval=1000)
    plt.show()