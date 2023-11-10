from tools import define
from tools import embedding
from llm.init_llm import init_llm 
import gischain.base as base
import gischain.showdag as sd
import gischain.check as check

CHECK_COUNT = 10 # 检查的次数

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
        if len(tools) > 0:
            return rundag(tools, show, multirun)
        
    # 运行大模型，并检查结果，返回工具列表
    def run_and_check(self, prompt, instruction):
        # 实际调用大模型，返回工具列表
        tools = self.llm.invoke(prompt)
        ok = False # 是否检查通过
        errors = "" # 检查出来的错误信息
        for i in range(CHECK_COUNT): # 控制一下，最多只检查若干次，要是仍然不对，则直接退出了
            ok,errors = check.check_tools(tools, instruction)
            if ok:
                break
            # 这里把errors也作为提示词，再次运行
            import json
            print(f"经过第{i+1}次检查，{errors}。")
            tools = self.llm.invoke(prompt, json.dumps(tools), errors)

        return ok, tools, errors

    # 运行大语言模型，得到要执行的工具列表
    def run_llm(self, instruction):
        descs,examples = embedding.select_tools(instruction, self.tools, self.llm.tool_token_len)
        # 构造提示词
        prompt = self.llm.build_prompt(instruction, descs, examples)
        # 给大模型返回结果，并检查，得到工具列表
        ok,tools,errors = self.run_and_check(prompt, instruction)
        return output_result(ok, tools, errors)
        
        
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

# 根据大模型返回的结果，和检查的结果，输出最终的结果
def output_result(ok, tools, errors):
    # 输出tools信息
    print(f"解析得到的工具有{len(tools)}个，列表和参数如下:")
    toolstr = [f'工具: {item}' for item in tools]
    print('\n'.join(toolstr))
    if ok:
        return tools
    else:
        print(f"经过多轮尝试，仍然存在无法绕过的错误，包括：{errors}")
        print(f"程序结束，请换大语言模型，或者修改任务指令。")
        return []