import zhipuai
from .llm import Llm

prompt = """
你现在是一个GIS领域专家和人工智能助手，现在要做一个gis领域的空间分析功能。
你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具(不要选用不上的工具)。
指令要求会比较复杂，请认真全面思考后给出解答。
并用JSON格式顺序列出对应的工具，请给出对应的输入信息，记得用户给出的数据目录，组合出完整的文件路径名。
由于要对接程序自动运行，除了JSON格式之外，绝对、绝对、绝对不要有多余的文字输出，任何多余的文字都是干扰项。
指令：{instruction}
工具集如下：
==========
{tools}
==========
"""

class ChatGLM(Llm):
    def set_api_key(self, key):
        zhipuai.api_key = key

    def build_prompt(self, instruction, tools):
        text  = prompt.format(instruction=instruction,tools=tools)
        print(f"输入给大语言模型的内容如下:{text}")
        return text

    def invoke(self, text):
        response = zhipuai.model_api.invoke(
            model="chatglm_pro", #  chatglm_std  chatglm_pro
            prompt=[{"role": "user", "content": text}],
            top_p=0.7,
            temperature=0.01,
        )
        content = response['data']['choices'][0]['content']
        return predeal(content)
        
# 把chatglm返回的字符串转换为工具集列表
def extract_content(string):
    index_left = string.find('[')
    index_right = string.find(']')
    return string[index_left+1:index_right]

def predeal(content:str):
    print(f"大语言模型的返回结果如下：\n{content}")
    content = extract_content(content) # 去掉前后的 []
    
    content = content.replace('\\n', '')
    content = content.replace('\\"', '\"')
    content = content.replace('\\t', '')
    content = content.strip()
    content = content.strip("\"")
    
    tools_str = "[" + content + "]"
    import json
    tool_list = json.loads(tools_str)
    return tool_list

