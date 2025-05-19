import json
from tools import define
from gischain.base import node_color_map, update_kv_dict
from . import base

# 处理一个任务结束时，应该修改的状态值、颜色值，并返回任务执行结果
def deal_one_task_done(shares, name, G):
    # 修改状态
    update_kv_dict(shares, name, {'status':'done', 'color':node_color_map.get(('task', 'done'))})
    # 修改output的状态
    outputs = G.successors(name)
    for output in outputs:
        output_name = output.get_name()
        update_kv_dict(shares, output_name, {'status':'ready', 'color':node_color_map.get(('data', 'ready'))})

    # 返回结果；增加判断，防止没有result属性的情况
    if "result" in shares[name]:
        return shares[name]["result"]
    else:
        return None

# 顺序执行list中的工具
def run_tools(tools, shares=None):
    # 按顺序执行工具list
    if shares != None:
        G = base.resotreDAG(shares)

    result = ""
    for tool in tools:
        task_name = None
        if shares != None:
            task_name = json.dumps(tool) 
            update_kv_dict(shares, task_name, {'status':'doing', 'color':node_color_map.get(('task', 'doing'))})
        # output = 
        # 去掉tool['parameters'] 中的 output属性
        # output = tool['parameters'].pop('output', None)
        # tool['parameters']['output'] = None
        result = define.call_tool(tool['name'], task_name, shares, **tool['parameters'])
        if shares != None:
            deal_one_task_done(shares, task_name, G)
    
    if shares != None:
        shares.update({"title":"GISChain run done."})
    return result

# ====================================================================================================

# 判断所有的工具是否都已经运行完毕
def is_all_tasks_done(shares):
    for key,node_data in shares.items():
        # 对于task节点，如果没有状态属性，或者状态不是 'done'，将标志变量设置为 False
        if base.is_node(key,shares) and node_data['type'] == 'task' and ('status' not in node_data or node_data['status'] != 'done'):
            return False
    return True

# 判断一个工具是否可以运行，即是否所有的input是否都已经ready
def task_is_ready(G,shares,name):
    inputs = G.predecessors(name)
    for input in inputs:
        input_name = input.get_name()
        if shares[input_name]["status"] != "ready":
            return False
    return True

# 根据名字，从tools列表中获取到tool对象
def find_tool(tools, name):
    for tool in tools:
        if tool['name'] == name:
            return tool
    return None

# 并行执行list中的工具
def multi_run_tools(tools, shares):
    import time
    import multiprocessing

    G = base.resotreDAG(shares)
    
    result = ""
    childs = []
    # 如果不是所有任务完成，则继续循环
    while is_all_tasks_done(shares) != True:
        # 遍历所有的task，找到可以运行的task
        for name, data in shares.items():
            # 1)是node，而非edge；2）是task；3）状态是 todo；4）所有的input都已经ready，则可以运行
            if base.is_node(name,shares) and data["type"] == "task" and data["status"] == "todo" and task_is_ready(G,shares,name) == True:
                update_kv_dict(shares, name, {'status':'doing', 'color':node_color_map.get(('task', 'doing'))})
                
                # 从shares的task名字中，恢复tool的信息
                tool = json.loads(name)
                # 启动子进程
                child_process = multiprocessing.Process(target=define.call_tool, args=(tool["name"], name, shares,tool['parameters']['output']), kwargs=tool['parameters'])
                child_process.start()
                childs.append((name, child_process))

        # 所有已经启动的子进程，只要有一个结束，就应该判断是否能启动下一个子进程
        for name, child_process in childs:
            if child_process.is_alive() == False:
                result = deal_one_task_done(shares, name, G)
                childs.remove((name, child_process))
                break
        
    shares.update({"title":"GISChain Run Done."})
    return result
