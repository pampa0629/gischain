# 基础能力放到这里，避免依赖关系混乱

import networkx as nx
import re, os
import json

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
    
# 眼色映射字典
node_color_map = {
    # R G B
    ("task", "todo"):  "lightblue", # 浅绿色
    # ("task", "ready"): "turquoise", # 绿松石色
    ("task", "doing"): "gold", # 金色
    ("task", "done"):  "violet", # 紫罗兰色
    
    ("data", "noready"): "lightgreen", # 浅蓝色
    ("data", "ready"): "teal", # 蓝绿色
}

# share 的数据结构
# { node_name1:
#       {‘type’:'task',
#        'status':'todo',
#        'tool':'buffer',
#        'color':'lightblue',
#        'result':filepath },
#   node_name2:{}, ...}
    
# 从 tools 中构造图，返回图和共享变量
# G 里面不再保存 task 的类型、状态、眼色和返回值等信息，只记录 node name 和 label（tool name）
def buildGaphic(tools):

    import multiprocessing
    manager = multiprocessing.Manager()
    shares = manager.dict()
    
    # 创建一个有向图
    G = nx.DiGraph()
    # 添加任务和其输入输出到图中
    for tool in tools:
        tool_name = tool["name"]
        # 这里要把tool的全部信息合并为一个字符串作为task的名字，否则会出现重名的情况
        task_name = json.dumps(tool) 

        # task 节点增加status属性，包括以下状态：
        #   todo  尚未处理，等到所有inputs都准备好后，就可以开始执行
        #   doing 正在执行中
        #   done  执行完毕
        G.add_node(task_name, lable=tool_name) # 显示用 lable 属性
        shares.update({task_name: {"tool":tool_name, "type":'task', "status":'todo', "color":node_color_map.get(('task', 'todo'))}})
        
        # data 节点增加status属性，包括以下状态：
        #   noready  尚未准备好，等待上游task的输出
        #   ready 已经准备好，可以为后续task使用
        inputs = tool["inputs"]
        for key,value in inputs.items():
            status = input_ready_status(key, value)
            G.add_node(value, lable=value)
            shares.update({value: {"type":'data', "status":status, "color":node_color_map.get(('data', status))}})
            # 对于 edge而言，区分input和output
            G.add_edge(value, task_name, type='input')
            
        output = tool["output"]
        G.add_node(output, lable=output)
        shares.update({output: {"type":'data', "status":'noready', "color":node_color_map.get(('data', 'noready'))}})
        G.add_edge(task_name, output, type='output')

    return G, shares

# 只修改部分属性，其他的仍然要保留
def update_kv_dict(shares, name, kv_dict):
    node_data = shares[name]
    node_data.update(kv_dict)
    shares.update({name: node_data})
