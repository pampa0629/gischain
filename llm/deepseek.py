# from openai import OpenAI
import openai
from http import HTTPStatus
from dashscope import Generation
# import dashscope
from .llm import Llm
from .prompt_template import build

class Deepseek(Llm):

    def set_api_key(self, key):
        openai.api_base = 'https://api.deepseek.com' # 固定不变
        openai.api_key = key 

    def build_prompt(self, instruction, tools, examples):
        return build(instruction, tools, examples, False, False)

    # deepseek  网址：https://api-docs.deepseek.com/zh-cn/ 
    def invoke(self, prompt, tools=None, errors=None):
        messages=[{'role': 'system', 'content': '你是GIS领域专家和人工智能助手。'},
                  {'role': 'user', 'content': prompt}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]

        client = openai.OpenAI(api_key=openai.api_key, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        print(response)
        content = response.choices[0].message.content
        print(content)
        from .base import predeal
        return predeal(content)

        
        # # print(response.choices[0].message.content)
        # if response.status_code == HTTPStatus.OK:
        #     content = response['output']['choices'][0]['message']['content']
        #     from .base import predeal
        #     return predeal(content)
        # else:
        #     print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
        #         response.request_id, response.status_code,
        #         response.code, response.message
        #     ))
        #     return None
