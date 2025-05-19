import json
from gischain import base

g_tools_mapping = {
#     "buffer": {"func":buffer(type:function),
#                "core":“{
#                         name:buffer,
#                         description:得到缓冲区,
#                         parameters:{                            
#                             datafile:要求缓冲区的数据文件,
#                             radius:缓冲区半径
#                             output:缓冲区结果文件
#                           }
#                     }”,
#                "example":"{}",
#                "check":check, # 增加对工具json的检查
#               },
#     "overlay": {},
#     "area": {},
}

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

def add_tool(name, func, core, example=None, check=None):
    g_tools_mapping[name] = {}
    g_tools_mapping[name]["func"] = func
    g_tools_mapping[name]["core"] = core    
    if example != None:
        g_tools_mapping[name]["example"] = example
    if check != None:
        g_tools_mapping[name]["check"] = check
    # 仅在主进程中输出工具的初始化信息
    if is_main_process():
        print(f"初始化工具 {name} 成功，内容为：{core}")

# 得到所有工具的名字
def get_tools_name():
    return list(g_tools_mapping.keys())

# 根据工具名字，得到工具的描述
def get_tool_desc(name):
    return get_tool_core(name)['description']
    # if name in g_tools_mapping:
    #     function = g_tools_mapping[name]
    #     return function["core"]['description']
    # else:
    #     print(f"没有找到名字为 {name} 的工具")
    #     return None
   
# 根据名字，得到工具的核心内容
def get_tool_core(name):
    if name in g_tools_mapping:
        function = g_tools_mapping[name]
        return function["core"]
    else:
        print(f"没有找到名字为 {name} 的工具")
        return None

# 根据工具名字，得到工具的例子
def get_tool_example(name):
    if name in g_tools_mapping:
        function = g_tools_mapping[name]
        if "example" in function:
            return function["example"]
    else:
        print(f"没有找到名字为 {name} 的工具")
    return ""

# 根据工具名字，和工具调用的json，检查工具调用是否正确
def check_tool(name, tool):
    if name in g_tools_mapping:
        function = g_tools_mapping[name]
        if "check" in function:
            return function["check"](tool)    
        return True, "" # 没有check函数，直接返回True    
    else:
        print(f"没有找到名字为 {name} 的工具")
        return False, f"没有在工具集中找到名字为{name}的工具，请必须使用工具集中提供的工具；"
    