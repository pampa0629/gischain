import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def buildGaphic():
    # 创建一个有向无环图（DAG）
    G = nx.DiGraph()
    G.add_node("Task1")
    G.add_node("Task2")
    G.add_node("Task3")
    G.add_node("Task4")
    G.add_node("Task5")
    G.add_edge("Task1", "Task2")
    G.add_edge("Task1", "Task3")
    G.add_edge("Task2", "Task4")
    G.add_edge("Task3", "Task4")
    G.add_edge("Task4", "Task5")

    return G
                
# 更新节点颜色的函数，这里使用随机颜色来模拟任务状态的变化
def update(frame, G, pos, task_colors):
    # for node in G.nodes():
    #     print("update node color:",task_colors[node])
    # pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=[task_colors[node] for node in G.nodes()], node_size=800, font_size=10, font_color='black')

def show_color(G,task_colors,update):    
    
    pos = nx.spring_layout(G, seed=42)
    # 创建一个初始绘图
    # def init():
    # nx.draw(G, pos, with_labels=True, node_color=[task_colors[node] for node in G.nodes()], node_size=800, font_size=10, font_color='black')
    
    # 创建动画
    ani = FuncAnimation(plt.figure(), update, fargs=(G,pos, task_colors,), frames=100, repeat=False, interval=1000)

    # 显示动画
    plt.show()

import multiprocessing
import time

if __name__ == "__main__":

    G = buildGaphic()    
    manager = multiprocessing.Manager()
    task_colors = manager.dict()
    # shared_dict["task_colors"] = task_colors
    task_colors.update({
        "Task1": "blue",
        "Task2": "blue",
        "Task3": "blue",
        "Task4": "blue",
        "Task5": "blue",
    })
    # pos = nx.spring_layout(G, seed=42)

    child_process = multiprocessing.Process(target=show_color,args=(G,task_colors,update))
        # 启动子进程
    child_process.start()

    print("child_process.pid:",child_process.pid)

    # 改变状态
    while True:
        time.sleep(2)
        for node in G.nodes():
            # print("while node:",node)
            if random.random() < 0.2:
                task_colors[node] = "green"  # 模拟任务完成
            elif random.random() < 0.3:
                task_colors[node] = "red"  # 模拟任务失败
            elif random.random() < 0.4:
                task_colors[node] = "yellow"  # 模拟任务运行中
            else:
                task_colors[node] = "blue"  # 模拟任务未运行
            
            print("while node color:",task_colors[node])

    child_process.join()