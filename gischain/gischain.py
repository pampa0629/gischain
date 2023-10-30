from tools import define
from llm.init_llm import init_llm 
import gischain.base as base
import gischain.showdag as sd

def init_gischain(llm="chatglm", key=None, tools=None):
    return GISChain(llm, key, tools)

class GISChain:
    def __init__(self, name="chatglm", key=None, user_tools=None) -> None:
        self.llm = init_llm(name, key)
        if self.llm != None:
            print(f"初始化大语言模型：{name} 成功")
        self.init_tools(user_tools)
    
    # 初始化工具集
    def init_tools(self, user_tools):
        # 先加载默认的tools
        all_tools = define.get_tools_name()
        # 再加载用户指定的tools
        if user_tools != None:
            all_tools.extend(user_tools)
        self.tools = all_tools

    # 运行用户指令
    def run(self, instruction, show=True, multirun=False):
        tools = self.run_llm(instruction)
        return rundag(tools, show, multirun)
    
    # 根据用户指令，通过向量化来选择工具集
    def select_tools(self, instruction, token_len=4096):
        from tools import embedding
        import numpy as np
        input = np.array(embedding.tongyi_emb(instruction))
        embs = define.get_tools_emb(self.tools)
        sorted_embs = embedding.sort_tools_by_CI(embs, input)
        descs = examples = ""
        # print("sorted_embs:")
        # print(sorted_embs)
        print("被选择的tool包括: ")
        tokens = 0
        for emb in sorted_embs:
            tool_name = emb["tool"]
            descs += define.get_tool_desc(tool_name)
            examples += define.get_tool_example(tool_name)
            tokens += emb["len"] # 粗略处理
            print(f"工具：{tool_name},CI:{emb['CI']},字符长度: {emb['len']}")
            if tokens >= token_len:
                break
        return descs,examples

    # 运行大语言模型，得到要执行的工具列表
    def run_llm(self, instruction):
        descs,examples = self.select_tools(instruction,self.llm.tool_token_len)
        # 构造提示词
        prompt = self.llm.build_prompt(instruction, descs, examples)
        # 运行，并根据结果，解析之后得到工具列表
        tools = self.llm.invoke(prompt)
        # 输出tools信息
        print(f"解析得到的工具有{len(tools)}个，列表和参数如下:")
        toolstr = [f'工具: {item}' for item in tools]
        print('\n'.join(toolstr))
        return tools
        
# 运行工具列表
def rundag(tools, show=True, multirun=False):
    # 要显示dag图或者多进程并行执行，需要先构造dag图
    if show or multirun:
        G, shares = base.buildGaphic(tools)
        
    if show:
        import multiprocessing
        child_process = multiprocessing.Process(target=sd.showdag, args=(G,shares,))
        # 启动子进程
        child_process.start()

    import gischain.runtools as runtools
    
    if multirun: # 多进程并行执行
        result = runtools.multi_run_tools(tools,G,shares)
    elif show : # 如果显示dag图，那么也要在执行过程中更新shares中的node状态
        result = runtools.run_tools(tools,G,shares)
    else:
        result = runtools.run_tools(tools)
    
    # 等待showdag的子进程结束
    if show:
        child_process.join()
    return result