import pygraphviz as pgv
import matplotlib.pyplot as plt

# 创建DAG
G = pgv.AGraph(directed=True)
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 7), (6, 8)])

# 使用Graphviz的布局引擎进行布局
G.layout(prog='dot')

# 使用matplotlib显示图形
plt.figure(figsize=(8, 6))
plt.axis('off')  # 不显示坐标轴
plt.title('Directed Acyclic Graph')

# 使用Graphviz的布局信息绘制图形
plt.plot()
plt.imshow(G.draw(format='png', prog='dot'), aspect='equal')
plt.show()
