from tools import define

# 顺序执行list中的工具
def run_tools(tools):
    # 按顺序，真正执行工具
    result = ""
    for tool in tools:
        # python只支持一个可变参数，这句话把output参数加上
        tool['inputs']['output'] = tool['output'] 
        result = define.call_tool(tool['name'], **tool['inputs'])
        print(f"工具 {tool['name']} 的执行结果为：{result}")
    return result

# 判断一个工具是否可以运行，即是否所有的input是否都已经ready
def task_is_ready(G, node):
    inputs = G.predecessors(node)
    ready = True
    for input in inputs:
        # print(input)
        # print(G.nodes[input])
        if G.nodes[input]["status"] != "ready":
            ready = False
            break
    return ready

# 判断所有的工具是否都已经运行完毕
def all_tasks_is_done(G):
    for node in G.nodes:
        if G.nodes[node]["type"] == "task" and G.nodes[node]["status"] != "done":
            return False
    return True

# 根据名字，从tools列表中获取到tool对象
def find_tool(tools, name):
    for tool in tools:
        if tool['name'] == name:
            return tool
    return None

# 并行执行list中的工具
def multi_run_tools(tools):

    from showdag import buildGaphic 
    import networkx as nx
    import multiprocessing

    # 创建一个有向图
    G = nx.DiGraph()
    buildGaphic(G, tools)
    
    # 创建一个共享变量，用于从子进程中获取结果
    manager = multiprocessing.Manager() 
    result_dict = manager.dict()

    result = ""
    # 如果不是所有任务完成，则继续循环
    while all_tasks_is_done(G) != True:
        childs = []
        for node in G.nodes:
            # 如果这个node是task，且状态是todo，且所有的input都已经ready，则可以运行
            if G.nodes[node]["type"] == "task" and G.nodes[node]["status"] == "todo" and task_is_ready(G, node) == True:
                G.nodes[node]["status"] = "doing"
                tool = find_tool(tools, node)
                # python只支持一个可变参数，这句话把output参数加上
                tool['inputs']['output'] = tool['output'] 
                # 启动子进程
                child_process = multiprocessing.Process(target=define.call_tool, args=(node,result_dict), kwargs=tool['inputs'])
                child_process.start()
                childs.append((node,child_process))

        for node, child_process in childs:
            # 等待子进程结束
            child_process.join()
            # 修改状态
            G.nodes[node]["status"] = "done"
            # 修改output的状态
            outputs = G.successors(node)
            for output in outputs:
                G.nodes[output]["status"] = "ready"
            result = result_dict[node]
            print(f"工具 {node} 的执行结果为：{result}")
            # print(f"工具 {node} 运行完毕")

    # 不要忘记最后显式关闭Manager对象
    manager.shutdown()
    return result
