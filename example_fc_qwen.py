from openai import OpenAI
from datetime import datetime
import json
import os
import random

import warnings
# 显示警告，但只显示一次
warnings.simplefilter("once")


import tools.buffer
import tools.overlay

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-f966cb8bbf914ec0b3dd3c1f771177fc",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)


import tools
# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
mytools = [
    # 工具1 buffer
    {
        "type": "function",
        "function": {
            "name": "buffer",
            "description": tools.buffer.desc,
            # buffer(datafile:str, radius:float, output:str):
            "parameters": {
                "type": "object",
                "properties": {
                    "datafile": {
                        "type": "string",
                        "description": "输入数据文件",
                    },
                    "radius": {
                        "type": "number",
                        "description": "缓冲区半径",
                    },
                    "output": {
                        "type": "string",
                        "description": "缓冲区结果文件",
                    },
                }
            }
        },
    },
    # 工具2 overlay
    {
        "type": "function",
        "function": {
            "name": "overlay",
            "description": tools.overlay.desc,
            # overlay(datafile1:str, datafile2:str, output:str):
            "parameters": {
                "type": "object",
                "properties": {
                    "datafile1": {
                        "type": "string",
                        "description": "输入数据文件1",
                    },
                    "datafile2": {
                        "type": "string",
                        "description": "输入数据文件2",
                    },
                    "output": {
                        "type": "string",
                        "description": "叠加结果文件",
                    },
                }
            }
        },
    },
]


# 封装模型响应函数
def get_response(messages):
    print("get_response：", messages,"\n")
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=mytools,
    )
    return completion


instruction = "修一条铁路，宽度为50米，需要计算占用周边的耕地面积。" # 260654505.39415726

mete_data = "耕地数据是 ./data/farmland.shp，铁路数据是 ./data/railway.shp；结果数据放到 ./data/output/ 目录下。"

# prompt = """你是gis专家，现在根据下面指令，以及提供的tools，确定需要用到的tools，
# 以及调用工具时，每个工具需要的参数，以及每个工具调用的顺序，请用json格式输出。记得把数据文件的路径组织好。指令为：
# """

def call_with_messages():
    print("call_with_messages\n")
    messages = [
        {
            "content": # input(
                instruction+mete_data,
            # ),  
            "role": "user",
        }
    ]
    print("-" * 60)
    # 模型的第一轮调用
    i = 1
    first_response = get_response(messages)
    assistant_output = first_response.choices[0].message
    print(f"\n第{i}轮大模型输出信息：{first_response}\n")
    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)
    # 如果不需要调用工具，则直接返回最终答案
    if (
        assistant_output.tool_calls == None
    ):  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        print(f"无需调用工具，我可以直接回复：{assistant_output.content}")
        return
    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while assistant_output.tool_calls != None:
        # 如果判断需要调用查询天气工具，则运行查询天气工具
        tool_info = {
            "content": "",
            "role": "tool",
            "tool_call_id": assistant_output.tool_calls[0].id,
        }
        if assistant_output.tool_calls[0].function.name == "buffer":
            # 提取位置参数信息
            
            print("buffer：", assistant_output.tool_calls[0].function.arguments)
            argumens = json.loads(assistant_output.tool_calls[0].function.arguments)
            print("buffer参数：", type(argumens))
            datafile  = argumens.get("datafile")
            radius  = argumens.get("radius")
            output  = argumens.get("output")
            print("buffer参数：", datafile, radius, output)
            tool_info["content"] = tools.buffer.buffer(datafile, radius, output)
        # 如果判断需要调用查询时间工具，则运行查询时间工具
        elif assistant_output.tool_calls[0].function.name == "overlay":
            print("overlay", assistant_output.tool_calls[0].function.arguments)
            argumens = json.loads(assistant_output.tool_calls[0].function.arguments)
            print("overlay参数：", argumens)
            tool_info["content"] = tools.overlay.overlay(argumens.get("datafile1"), argumens.get("datafile2"), argumens.get("output"))
        tool_output = tool_info["content"]
        print(f"工具输出信息：{tool_output}\n")
        print("-" * 60)
        messages.append(tool_info)
        assistant_output = get_response(messages).choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
        i += 1
        print(f"第{i}轮大模型输出信息：{assistant_output}\n")
    print(f"最终答案：{assistant_output.content}")


if __name__ == "__main__":
    call_with_messages()