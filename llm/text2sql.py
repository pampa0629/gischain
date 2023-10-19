import requests
import json
from .llm import Llm

prompt = """
你现在是一个GIS领域专家和人工智能助手，现在要做一个gis领域的空间分析功能。
你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具(不要选用不上的工具)。
工具集如下：
==========
{tools}
==========
指令：{instruction}
指令要求比较复杂，请认真全面思考后给出解答。
并用JSON格式顺序列出对应的工具，请给出对应的输入信息；
输入数据放在data目录下，中间生成的文件放在temp目录下，最终结果放在output目录下，记得组合出正确的相对文件路径。
由于要对接程序自动运行，除了JSON格式之外，绝对、绝对、绝对不要有多余的文字输出，任何多余的文字都是干扰项。
"""

import requests

class Text2SQL(Llm):
    def set_api_key(self, key):
        self.key = key

    def build_prompt(self, instruction, tools):
        text  = prompt.format(instruction=instruction,tools=tools)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text):
        url = 'http://1229992103460597.cn-shanghai.pai-eas.aliyuncs.com/api/predict/text2sql/v1/chat/completions'
        headers = {
            'Authorization': self.key,
            'Content-Type': 'application/json'
        }
        data = {
            "model": "text2sql",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "max_tokens": 2048,
            "temperature": 0
        }

        response = requests.post(url, headers=headers, json=data)

        # 检查HTTP响应状态码
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            content = extract_content(content)
            # 去掉[]外面的内容，再构建json list
            tools_str = "[" + content + "]"
            tool_list = json.loads(tools_str)
            return tool_list
        else:
            print("text2sql请求失败，状态码:", response.status_code)
            return None
            

# 去掉字符串中的前后[]，再构建json list
def extract_content(string):
    index_left = string.find('[')
    index_right = string.find(']')
    return string[index_left+1:index_right]