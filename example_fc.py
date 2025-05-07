from openai import OpenAI
from datetime import datetime
import json
import os
import random

import warnings
# 显示警告，但只显示一次
# warnings.simplefilter("once")
warnings.filterwarnings("ignore")


import tools.buffer
import tools.overlay

client = OpenAI(
    # base_url='https://api.openai-proxy.org/v1',
    # api_key='sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm',
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
    # 工具 filter
    {
        "type": "function",
        "function": {
            "name": "filter",
            "description": tools.filter.desc,
            # def filter(datafile:str, where:str, output:str):
            "parameters": {
                "type": "object",
                "properties": {
                    "datafile": {
                        "type": "string",
                        "description": "输入数据文件",
                    },
                    "where": {
                        "type": "string",
                        "description": "过滤条件",
                    },
                    "output": {
                        "type": "string",
                        "description": "过滤结果文件",
                    }
                }
            }
        },
    },
    # 工具 dissolve
    {
        "type": "function",
        "function": {
            "name": "dissolve",
            "description": tools.dissolve.desc,
            # def dissolve(datafile:str, output:str):
            "parameters": {
                "type": "object",
                "properties": {
                    "datafile": {
                        "type": "string",
                        "description": "需要进行融合的数据文件",
                    },
                    "output": {
                        "type": "string",
                        "description": "融合后的数据文件",
                    }
                }
            }
        },
    },
    # 工具 area
    {
        "type": "function",
        "function": {
            "name": "area",
            "description": tools.area.desc,
            # def area(datafile:str, output=None) -> float:
            "parameters": {
                "type": "object",
                "properties": {
                    "datafile": {
                        "type": "string",
                        "description": "要求面积的数据文件",
                    },
                    "output": {
                        "type": "string",
                        "description": "面积结果文件，json格式",
                    }
                }
            }
        },
    },
# 工具 ratio
    {
        "type": "function",
        "function": {
            "name": "ratio",
            "description": tools.ratio.desc,
            #  def ratio(value1:str, value2:str,output=None):
            "parameters": {
                "type": "object",
                "properties": {
                    "value1": {
                        "type": "string",
                        "description": "第一个数值",
                    },
                    "value2": {
                        "type": "string",
                        "description": "第二个数值",
                    },
                    "output": {
                        "type": "string",
                        "description": "结果文件，json格式",
                    }
                }
            }
        },
    },
]


# 封装模型响应函数
def get_response(messages):
    print("get_response：", messages,"\n")
    completion = client.chat.completions.create(
        # model="gpt-4o-mini",
        model="qwen-plus",
        messages=messages,
        tools=mytools,
        tool_choice="auto"
    )
    return completion


# instruction = "修一条铁路，宽度为50米，需要计算占用周边的耕地面积。" # 260654505.39415726
presume = "假定：步行五分钟能走300米，公园绿地类型的编码为1201,记得中间需要做数据融合。"
instruction = presume + "计算南京市公园绿地步行五分钟的范围，占市区范围面积的比率。" 

# mete_data = "耕地数据是 ./data/farmland.shp，铁路数据是 ./data/railway.shp；结果数据放到 ./data/output/ 目录下。"
# "规划用地.shp":{
#         "description":"南京市规划用地",
#         "fields":{
#             "YDFLDM":"用地类型"
#         }
#     },
#     "城区范围.shp":{
#         "description":"南京市城区范围"
#     }
mete_data = "规划用地是 ./data/规划用地.shp，用地类型字段是“YDFLDM”；城区范围是 ./data/城区范围.shp；结果数据放到 ./data/output/ 目录下。"

system_prompt = f"""
You are a friendly chatbot that can use external tools to offer reliable assistance to human beings.
"""

# prompt = """你是gis专家，现在根据下面指令，以及提供的tools，确定需要用到的tools，
# 以及调用工具时，每个工具需要的参数，以及每个工具调用的顺序，请用json格式输出。记得把数据文件的路径组织好。指令为：
# """

from tools import define
def call_with_messages():
    print("call_with_messages\n")
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "content": # input(
                instruction+mete_data,
            # ),  
            "role": "user",
        }
    ]
    json_tools = []
    i = 1
    while True:
        print("-" * 60)
        response = get_response(messages)
        print(f"\n第{i}轮大模型输出信息：{response}\n")
        i = i+1
    
        response_msg = response.choices[0].message
        messages.append(response_msg)
        print(response_msg.content) if response_msg.content else print(response_msg.tool_calls)
    
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "stop":
            break
    
        tool_calls = response_msg.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                print(f"调用工具：{function_name}，参数：{function_args}")
                json_tools.append(
                    {
                        "name": function_name,
                        "args": function_args
                    }
                )
                # function_response = define.call_tool(function_name, None,None, **function_args)
                function_response =function_args['output']
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response)
                    }
                )

    # 真正执行tools
    for tool in json_tools:
        print(tool)
        define.call_tool(tool['name'], None,None, **tool['args'])


if __name__ == "__main__":
    call_with_messages()