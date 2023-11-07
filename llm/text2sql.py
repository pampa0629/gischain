import requests
import json
from .llm import Llm
# from .prompt_en import prompt
# from .prompt_en import example1_desc, example1_json, example2_desc, example2_json

prompt = """
You are now an expert in the GIS field and an AI assistant. 
Your task is to perform a spatial analysis function in the GIS domain. 
You must follow instructions to complete a specific task, selecting the appropriate tools from the toolset provided (do not use unnecessary tools).

The toolset is as follows:
{tools}

{examples}

Instructions: {instruction}

The instructions are quite complex, so please carefully consider all aspects before providing a solution. 
List the corresponding tools in JSON format and include the input information.
Input data should be located in the 'data' directory, intermediate files in the 'data/temp' directory, and the final results in the 'data/output' directory. 
Ensure that you construct the correct relative file paths.
Since this needs to integrate with a program for automated execution, there should be absolutely no extra textual output beyond the JSON format. 
Any extra text is considered noise.
"""

import requests

class Text2SQL(Llm):
    def set_api_key(self, key):
        self.key = key

    def build_prompt(self, instruction, tools, examples):
        examples = f"The examples of toolset are as follows:\n{examples}"
        text  = prompt.format(instruction=instruction, tools=tools, examples="")
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text, tools=None, errors=None):
        messages =  [{"role": "user","content": text}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]
        
        url = 'http://1229992103460597.cn-shanghai.pai-eas.aliyuncs.com/api/predict/text2sql/v1/chat/completions'
        headers = {
            'Authorization': self.key,
            'Content-Type': 'application/json'
        }
        data = {
            "model": "text2sql",
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.01
        }

        response = requests.post(url, headers=headers, json=data)

        # 检查HTTP响应状态码
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            from .base import predeal
            return predeal(content)
        else:
            print("text2sql请求失败，状态码:", response.status_code)
            return None
            