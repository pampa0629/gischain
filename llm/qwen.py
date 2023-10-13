from http import HTTPStatus
from dashscope import Generation
import dashscope
from .llm import Llm

prompt="""
现在要做一个gis领域的空间分析功能。
你需要按照给出的要求完成任务，从下面工具集中选择合适的工具(不要选用不上的工具)，
并用JSON格式顺序列出对应的工具，请给出对应的输入信息；
输入数据放在data目录下，中间生成的文件放在temp目录下，最终结果放在output目录下，记得组合出完整的文件路径名。
由于要对接程序自动运行，不要有任何多余的文字输出，多余的文字都是干扰项。
要求：{instruction}
工具集如下：
==========
{tools}
==========
"""
class QWen(Llm):

    def set_api_key(self, key):
        dashscope.api_key=key

    def build_prompt(self, instruction, tools):
        text  = prompt.format(instruction=instruction,tools=tools)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, prompt):
        messages = [{'role': 'system', 'content': '你是GIS领域专家和人工智能助手。'},
                    {'role': 'user', 'content': prompt}]
        gen = Generation()
        response = gen.call(
            Generation.Models.qwen_turbo,
            messages=messages,
            result_format='message',  # set the result to be "message" format.
        )
        
        if response.status_code == HTTPStatus.OK:
            content = response['output']['choices'][0]['message']['content']
            return predeal(content)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None

def predeal(content:str):
    print(f"大语言模型的返回结果如下：\n{content}")
    tools_str = "[" + content + "]"
    import json
    tool_list = json.loads(tools_str)
    return tool_list