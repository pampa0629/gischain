from tools import define
from llm.init_llm import init_llm 

def init_gischain(llm="chatglm", key=None, tools=None):
    return GISChain(llm, key, tools)

class GISChain:
    def __init__(self, name="chatglm", key=None, tools=None) -> None:
        self.llm = init_llm(name, key)
        if self.llm != None:
            print(f"初始化大语言模型：{name} 成功")
        self.init_tools(tools)
    
    # 初始化工具集
    def init_tools(self, tools):
        # 先加载默认的tools
        all_tools = define.get_tools_name()
        # 再加载用户指定的tools
        if tools != None:
            all_tools.extend(tools)
        # 最后把tools的描述信息拼接起来
        discs = ""
        for tool in all_tools:
            discs += define.get_tool_disc(tool)
        self.discs = discs

    # 运行用户指令
    def run(self, instruction):
        tools = self.run_llm(instruction)
        
        # 按顺序，真正执行工具
        result = ""
        for tool in tools:
            # python只支持一个可变参数，这句话把output参数加上
            tool['inputs']['output'] = tool['output'] 
            result = define.call_tool(tool['name'], **tool['inputs'])
            print(f"工具 {tool['name']} 的执行结果为：{result}")
        return result

    # 运行大语言模型，得到要执行的工具列表
    def run_llm(self, instruction):
        # 构造提示词
        prompt = self.llm.build_prompt(instruction, self.discs)
        # 运行，并根据结果，解析之后得到工具列表
        tools = self.llm.invoke(prompt)
        # 输出tools信息
        print(f"解析得到的工具有{len(tools)}个，列表和参数如下:")
        toolstr = [f'工具: {item}' for item in tools]
        print('\n'.join(toolstr))
        return tools
        
        