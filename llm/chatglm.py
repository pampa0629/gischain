import zhipuai
from .llm import Llm
from .prompt_template import build

class ChatGLM(Llm):
    def set_api_key(self, key):
        zhipuai.api_key = key

    def build_prompt(self, instruction, tools, examples):
        return build(instruction, tools, examples, True, False)
        
    def invoke(self, text, tools=None, errors=None):
        prompt=[{'role': 'user', 'content': text}]
        if tools!=None:
            prompt+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            prompt+=[{'role': 'user', 'content': errors}]

        response = zhipuai.model_api.invoke(
            model="chatglm_pro", #  chatglm_std  chatglm_pro
            prompt=prompt,
            temperature=0.01
        )
        content = response['data']['choices'][0]['content']
        return predeal(content)
        

# 把chatglm返回的字符串转换为工具集列表
from  .base import extract_content
import json
def predeal(content:str):
    print(f"大语言模型的返回结果如下：\n{content}")
    content = extract_content(content) # 去掉前后的 []
    
    content = content.replace('\\n', '')
    content = content.replace('\\"', '\"')
    content = content.replace('\'', '\"')
    content = content.replace('\\t', '')
    content = content.strip()
    # content = content.strip("\"")
    content = content.rstrip(",") # 去掉最后一个逗号
    
    tools_str = "[" + content + "]"
    tool_list = json.loads(tools_str)
    return tool_list

