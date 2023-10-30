import json
from tools import define
from gischain.base import node_color_map, update_kv_dict


# 处理一个任务结束时，应该修改的状态值、颜色值，并返回任务执行结果
def deal_one_task_done(shares, name, G):
    # 修改状态
    update_kv_dict(shares, name, {'status':'done', 'color':node_color_map.get(('task', 'done'))})
    # 修改output的状态
    outputs = G.successors(name)
    for output in outputs:
        update_kv_dict(shares, output, {'status':'ready', 'color':node_color_map.get(('data', 'ready'))})

    # 返回结果；增加判断，防止没有result属性的情况
    if "result" in shares[name]:
        return shares[name]["result"]
    else:
        return None

# 顺序执行list中的工具
def run_tools(tools, G=None, shares=None):
    # 按顺序执行工具list
    result = ""
    for tool in tools:
        if G != None and shares != None:
            task_name = json.dumps(tool) 
        result = define.call_tool(tool['name'], task_name, shares,tool['output'], **tool['inputs'])
        if G != None and shares != None:
            deal_one_task_done(shares, task_name, G)
        
    return result

# ====================================================================================================

# 判断所有的工具是否都已经运行完毕
def is_all_tasks_done(shares):
    for node_data in shares.values():
        # 对于task节点，如果没有状态属性，或者状态不是 'done'，将标志变量设置为 False
        if node_data['type'] == 'task' and ('status' not in node_data or node_data['status'] != 'done'):
            return False
    return True

# 判断一个工具是否可以运行，即是否所有的input是否都已经ready
def task_is_ready(G,shares,name):
    inputs = G.predecessors(name)
    for input in inputs:
        if shares[input]["status"] != "ready":
            return False
    return True

# 根据名字，从tools列表中获取到tool对象
def find_tool(tools, name):
    for tool in tools:
        if tool['name'] == name:
            return tool
    return None

# 并行执行list中的工具
def multi_run_tools(tools, G, shares):
    import networkx as nx
    import multiprocessing
    
    result = ""
    # 如果不是所有任务完成，则继续循环
    while is_all_tasks_done(shares) != True:
        childs = []
        for name, data in shares.items():
            # 如果这个node是task，且状态是 todo，且所有的input都已经ready，则可以运行
            if data["type"] == "task" and data["status"] == "todo" and task_is_ready(G,shares,name) == True:
                update_kv_dict(shares, name, {'status':'doing', 'color':node_color_map.get(('task', 'doing'))})
                
                # 从shares的task名字中，恢复tool的信息
                tool = json.loads(name)
                # 启动子进程
                child_process = multiprocessing.Process(target=define.call_tool, args=(tool["name"], name, shares,tool['output']), kwargs=tool['inputs'])
                child_process.start()
                childs.append((name, child_process))

        for name, child_process in childs:
            # 等待子进程结束
            child_process.join()
            result = deal_one_task_done(shares, name, G)

    return result