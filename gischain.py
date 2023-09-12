from llm import chatglm
from tools import define

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
    def __init__(self, key, llm="chatglm", tools=None) -> None:
        self.llm = llm
        chatglm.set_api_key(key)
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
        print(f"输入给大语言模型的内容如下:{text}")
        tools = chatglm.invoke_llm(text)
        print(f"解析得到的工具有{len(tools)}个，列表和参数如下:")
        toolstr = [f'工具: {item}' for item in tools]
        print('\n'.join(toolstr))

        result = ""
        for tool in tools:
            # python只支持一个可变参数，这句话把output参数加上
            tool['inputs']['output'] = tool['output'] 
            result = define.call_tool(tool['name'], **tool['inputs'])
            print(f"工具 {tool['name']} 的执行结果为：{result}")
        return result

def init_gischain(key, llm="chatglm", tools=None):
    return GISChain(key, llm, tools)
    