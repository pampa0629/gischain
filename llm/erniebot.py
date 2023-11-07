import requests
import json
from .llm import Llm
from .prompt import build

class ErnieBot(Llm):
    def __init__(self):
        super().__init__()  # 调用父类的初始化方法
        self.tool_token_len = 2048 

    def set_api_key(self, key):
        # 文心一言，需要ak和sk
        self.ak = key['ak']
        self.sk = key['sk']
        self.token = self.get_access_token()

    def build_prompt(self, instruction, tools, examples):
        # 文心一言对输入的tokenliang有限制，所以就不再输入工具的范例了
        return build(instruction, tools, "", False, False)

    def invoke(self, text, tools=None, errors=None):
        messages =  [{"role": "user","content": text}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + self.token        
        payload = json.dumps({
            "messages": messages,
            "temperature": 0.01 # 降低随机性，使得结果更加稳定
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = json.loads(response.text)
        from .base import predeal
        return predeal(content["result"])

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.ak, "client_secret": self.sk}
        return str(requests.post(url, params=params).json().get("access_token"))
