import openai
from .llm import Llm

# gpt4 就是这么神奇，无需更多的提示词工程，就能输出正确结果

prompt = """
你现在是一个GIS领域专家和人工智能助手，现在要做一个gis领域的空间分析功能。
你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具；用不上的工具不要选，有些工具可能会被使用多次。
指令要求会比较复杂，请认真全面思考，一步步的完成，全部步骤可能会有5到10个步骤，甚至更多。
用JSON格式顺序列出要使用的工具，请给出对应的输入信息；
输入数据放在data目录下，中间生成的文件放在data/temp目录下，最终结果放在data/output目录下，记得组合出完整的文件路径名。
由于要对接程序自动运行，不要有多余的文字输出，任何多余的文字都是干扰项。
指令：{instruction}
工具集如下：
==========
{tools}
==========
{examples}
"""

# https://platform.openai.com/docs/models/gpt-4

class GPT4(Llm):
    def __init__(self):
        super().__init__()  # 调用父类的初始化方法
        # self.tool_token_len = 8192 

    def set_api_key(self, key):
        openai.api_base = 'https://api.closeai-asia.com/v1' # 固定不变
        openai.api_key = key 

    def build_prompt(self, instruction, tools, examples):
        examples = f" 工具集的使用范例如下：\n“““\n{examples}\n””” " # gpt4用不着例子也能搞定
        text  = prompt.format(instruction=instruction,tools=tools, examples=examples)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text, tools=None, errors=None):
        messages=[{"role": "system", "content": "You are a GIS domain expert and a helpful assistant."},
                      {"role": "user", "content": text}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview", # gpt-4-1106-preview gpt-4
            messages=messages,
            temperature=0.01)
        content = response.choices[0].message.content
        from .base import predeal
        return predeal(content)

