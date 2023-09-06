from llm import chatglm
from tools import define
# from . import tools

prompt = """
你现在是一个人工智能助手，现在要做一个gis领域的空间分析功能。
你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具(不要选用不上的工具)，
并用JSON格式顺序列出对应的工具，请给出对应的输入信息，记得组合出完整的文件路径名。
由于要对接程序自动运行，不要有任何多余的文字输出，多余的文字都是干扰项。
指令：{instruction}
工具集如下：
==========
{tools}
==========
"""

class GISChain:
    def __init__(self, llm="chatglm", tools=None) -> None:
        self.llm = llm
        if tools == None:
            tools = define.get_tools_name()
            discs = ""
            for tool in tools:
                discs += define.get_tool_disc(tool)
            self.discs = discs

    def run(self, instruction):
        # 构造一下提示词
        global prompt
        text  = prompt.format(instruction=instruction,tools=self.discs)
        print("to llm text:",text)
        tools = chatglm.invoke_llm(text)
        print("tools:",type(tools),len(tools),tools)
        result = ""
        for tool in tools:
            print(tool)
            tool['inputs']['output'] = tool['output']
            result = define.call_tool(tool['name'], **tool['inputs'])
            print(result)
        return result

def init_gischain(llm="chatglm", tools=None):
    return GISChain(llm, tools)
    