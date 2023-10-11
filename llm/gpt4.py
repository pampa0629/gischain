import openai
from .llm import Llm

prompt = """
你现在是一个GIS领域专家和人工智能助手，现在要做一个gis领域的空间分析功能。
你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具；用不上的工具不要选，有些工具可能会被使用多次。
指令要求会比较复杂，请认真全面思考，一步步的完成，全部步骤可能会有5到10个步骤，甚至更多。
用JSON格式顺序列出要使用的工具，请给出对应的输入信息，记得组合出完整的文件路径名。
由于要对接程序自动运行，不要有多余的文字输出，任何多余的文字都是干扰项。
指令：{instruction}
工具集如下：
==========
{tools}
==========
"""

# https://platform.openai.com/docs/models/gpt-4

class GPT4(Llm):
    def set_api_key(self, key):
        openai.api_base = 'https://api.closeai-asia.com/v1' # 固定不变
        openai.api_key = key 

    def build_prompt(self, instruction, tools):
        text  = prompt.format(instruction=instruction,tools=tools)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-4", # gpt-4 
            messages=[{"role": "user", "content": text}])
        content = response.choices[0].message.content
        print(f"大语言模型的返回结果如下：\n{content}")
        import json
        tool_list = json.loads(content)
        return tool_list
        

