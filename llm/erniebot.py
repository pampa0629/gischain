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

class ErnieBot(Llm):
    def set_api_key(self, key):
        # 文心一言，需要ak和sk
        self.ak = key['ak']
        self.sk = key['sk']

    def build_prompt(self, instruction, tools):
        text  = prompt.format(instruction=instruction,tools=tools)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text):
        token = self.get_access_token()
        # ERNIE-Bot-4 
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + token
        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + token
        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "temperature": 0.01 # 降低随机性，使得结果更加稳定
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print("response text:")
        print(response.text)

        content = json.loads(response.text)

        result = content["result"]
        print("result:")
        print(result)
        tools_content = extract_content(result)
        print("tools_content:")
        print(tools_content)
        # 去掉[]外面的内容，再构建json list
        tools_str = "[" + tools_content + "]"
        tool_list = json.loads(tools_str)
        return tool_list

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.ak, "client_secret": self.sk}
        return str(requests.post(url, params=params).json().get("access_token"))

# 去掉字符串中的前后[]，再构建json list
def extract_content(string):
    index_left = string.find('[')
    index_right = string.find(']')
    return string[index_left+1:index_right]