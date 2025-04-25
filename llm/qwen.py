from http import HTTPStatus
from dashscope import Generation
import dashscope
from .llm import Llm
from .prompt_template import build

class QWen(Llm):

    def set_api_key(self, key):
        dashscope.api_key=key

    def build_prompt(self, instruction, tools, examples):
        return build(instruction, tools, examples, False, False)

    # 通义千问 api 网址：https://dashscope.console.aliyun.com/apiKey 
    def invoke(self, prompt, tools=None, errors=None):
        messages=[{'role': 'system', 'content': '你是GIS领域专家和人工智能助手。'},
                  {'role': 'user', 'content': prompt}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]

        gen = Generation()
        response = gen.call(
            # 
            Generation.Models.qwen_max, #   qwen_turbo qwen_plus qwen_max qwen-max-latest
            messages=messages,
            temperature=0.01,
            result_format='message',  # set the result to be "message" format.
        )
        
        if response.status_code == HTTPStatus.OK:
            content = response['output']['choices'][0]['message']['content']
            from .base import predeal
            return predeal(content)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None
