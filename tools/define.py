# from tools import buffer,overlay,area
import json

g_tools_mapping = {
#     "buffer": {"func":buffer,
#               "desc":“{
#                         name:buffer,
#                         description:得到缓冲区,
#                         inputs:{
#                             datafile:要求缓冲区的数据文件
#                             radius:缓冲区半径
#                             },
#                         output:缓冲区结果文件
#                     }”,
#               "example":“{}
#     "overlay": {},
#     "area": {},
}

g_tools_emb = []
# [{"tool": "buffer","emb":[],"len":123},]

from gischain import base

def call_tool(tool_name, node_name, result_dict, output, **kwargs):
    if tool_name in g_tools_mapping:
        func = g_tools_mapping[tool_name]["func"]
        print(f"开始运行工具 {tool_name} ，参数为：{kwargs}")
        # python只支持一个可变参数，这句话把output参数加上
        kwargs["output"] = output
        result = func(**kwargs)
        if result_dict != None:        
            base.update_kv_dict(result_dict, node_name, {"result":result})
            
        print(f"工具 {tool_name} 执行结束，输出为：{result}")
        return result
    else:
        print(f"没有找到名字为 {tool_name} 的工具")
        return None

import multiprocessing

def is_main_process():
    return multiprocessing.current_process().name == "MainProcess"

def add_tool(name, func, desc, example=None):
    g_tools_mapping[name] = {}
    g_tools_mapping[name]["func"] = func
    g_tools_mapping[name]["desc"] = desc
    if example != None:
        g_tools_mapping[name]["example"] = example
    # 仅在主进程中输出工具的初始化信息
    if is_main_process():
        print(f"初始化工具 {name} 成功，内容为：{desc}")

def get_tool_desc(name):
    if name in g_tools_mapping:
        function = g_tools_mapping[name]
        return function["desc"]
    else:
        print(f"没有找到名字为 {name} 的工具")
        return None
    
def get_tool_example(name):
    if name in g_tools_mapping:
        function = g_tools_mapping[name]
        if "example" in function:
            return function["example"]
    else:
        print(f"没有找到名字为 {name} 的工具")
    return ""

# 根据工具名字，获取单个工具的embedding
def get_tool_emb(name):
    # print("get_tool_emb:",name)
    # print("g_tools_emb:",len(g_tools_emb))
    for tool_emb in g_tools_emb:
        if tool_emb["tool"] == name:
            return tool_emb
    print(f"没有找到名字为 {name} 的工具")
    return None

# 根据tools的名字，获取embedding
def get_tools_emb(tools):
    result = []
    for tool in tools:
        emb = get_tool_emb(tool)
        if emb != None:
            result.append(emb)
    return result
    
def get_tools_name():
    return list(g_tools_mapping.keys())

def init_tools_emb():
    from .embedding import load_tools_emb
    tools_emb = load_tools_emb()
    g_tools_emb.extend(tools_emb)
    # print("初始化工具的embedding:",len(g_tools_emb))
    for tool_emb in g_tools_emb:
        tool_name = tool_emb["tool"]
        tool_emb["len"] = len(g_tools_mapping[tool_name]["desc"]) + len(g_tools_mapping[tool_name]["example"])
