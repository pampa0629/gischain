# from tools import buffer,overlay,calculateArea
import json

tools_mapping = {
    # "buffer": {"func":buffer,"dics":“{
    #                                     name:buffer,
    #                                     discription:得到缓冲区,
    #                                     inputs:{
    #                                         datafile:要求缓冲区的数据文件
    #                                         radius:缓冲区半径
    #                                         },
    #                                     output:缓冲区结果文件
    #                                 }”,
    # # "overlay": overlay,
    # "calculateArea": calculateArea,
}

def call_tool(name, **kwargs):
    if name in tools_mapping:
        func = tools_mapping[name]["func"]
        print(f"开始运行工具 {name} ，参数为：{kwargs}")
        return func(**kwargs)
    else:
        print(f"没有找到名字为 {name} 的工具")
        return None

def add_tool(name, func, disc):
    tools_mapping[name] = {}
    tools_mapping[name]["func"] = func
    tools_mapping[name]["disc"] = disc
    print(f"初始化工具 {name} 成功，内容为：{disc}")

def get_tool_disc(name):
    if name in tools_mapping:
        function = tools_mapping[name]
        return function["disc"]
    else:
        print(f"没有找到名字为 {name} 的工具")
        return None
    
def get_tools_name():
    return list(tools_mapping.keys())