from tools import define, fc
from llm.init_llm import init_llm 
import gischain.base as base
import gischain.showdag as showdag
import gischain.check as check
import gischain.selecttools as select
import gischain.data as data
import json

CHECK_COUNT = 10 # 检查的次数
BASE_TOKEN_LEN = 500 # 基础的token长度

def init_gischain(llm="chatglm", key=None, funcall=False, tools=None):
    return GISChain(llm, key, funcall, tools)

class GISChain:
    def __init__(self, name="chatglm", key=None, funcall=False, user_tools=None) -> None:
        self.llm = init_llm(name, key, funcall)
        self.funcall = funcall
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
    # instruction: 用户指令
    # funcall:是否使用function call
    # show: 是否显示DAG图
    # multirun: 是否多线程运行
    def run(self, instruction, show=True, multirun=False):
        tools = self.run_llm(instruction,self.funcall)
        if len(tools) > 0:
            return rundag(tools, show, multirun)
        
    # 调用大模型，并检查结果，返回工具列表
    def invoke_and_check(self, prompt, instruction, data_descs):
        # 实际调用大模型，返回工具列表
        tools = self.llm.invoke(prompt)
        ok = False # 是否检查通过
        errors = "" # 检查出来的错误信息
        for i in range(CHECK_COUNT): # 控制一下，最多只检查若干次，要是仍然不对，则直接退出了
            ok,errors = check.check_tools(tools, instruction, data_descs)
            if ok:
                break
            # 这里把errors也作为提示词，再次运行
            import json
            print(f"经过第{i+1}次检查，{errors}。")
            tools = self.llm.invoke(prompt, json.dumps(tools), errors)

        return ok, tools, errors

    # 运行大语言模型，得到要执行的工具列表
    def run_llm(self, instruction, funcall=False):
        # 通过大模型，根据任务指令，刷选出需要的数据
        data_descs = data.select_data(self.llm, instruction)
        instruction = f"{instruction}；数据的json描述为：{data_descs}" # 把数据信息加入到指令中
        # 通过大模型，初步筛选工具
        selected_tools = select.select_tools(self.llm, instruction, self.tools)

        if funcall : # 用function call方式来获取工具列表
            return self.get_tools_with_funcall(instruction, selected_tools)
        else : 
            return self.get_tools_with_prompt(instruction, data_descs, selected_tools)
    
    # 用function call方式来获取工具列表
    def get_tools_with_funcall(self, instruction, selected_tools):
        print("通过function call方式来获取工具列表")

        tools_obj = [] # 根据名字，构建符合fc格式的工具对象
        for name in selected_tools:
            tools_obj.append(fc.build_fc_obj(define.get_tool_core(name)))
        
        messages = self.llm.build_prompt(instruction, None, None)
        json_tools = []
        i = 1
        while True:
            print("-" * 60)
            response = self.llm.invode_with_fc(messages, tools_obj)
            print(f"\n第{i}轮大模型输出信息：{response}\n")
            i = i+1
        
            response_msg = response.choices[0].message
            messages.append(response_msg)
            print(response_msg.content) if response_msg.content else print(response_msg.tool_calls)
        
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break
        
            tool_calls = response_msg.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"调用工具：{function_name}，参数：{function_args}")
                    # 先记录下来
                    json_tools.append(
                        {
                            "name": function_name,
                            "parameters": function_args
                        }
                    )
                    function_response =function_args['output']
                    
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": str(function_response)
                        }
                    )
        return json_tools

    # 通过提示词给大模型来得到工具列表
    def get_tools_with_prompt(self, instruction, data_descs, selected_tools):
    # 通过大模型，初步筛选工具，得到对应的工具描述和示例
        tools_descs, examples = select.get_tools_and_example(selected_tools, self.llm.token_len - BASE_TOKEN_LEN)
        # 构造提示词
        prompt = self.llm.build_prompt(instruction, tools_descs, examples)
        # 通过大模型返回工具列表，并检查
        ok,tools,errors = self.invoke_and_check(prompt, instruction, data_descs)
        # 根据检查是否ok，输出工具列表
        return output_result(ok, tools, errors)
    
# 运行工具列表
def rundag(tools, show=True, multirun=False):
    # 要显示dag图或者多进程并行执行，需要先构造dag图
    if show or multirun:
        shares = base.buildShares(tools)
        
    if show: 
        import multiprocessing
        child_process = multiprocessing.Process(target=showdag.show, args=(shares,))
        # 启动子进程
        child_process.start()

    import gischain.runtools as runtools
    
    if multirun: # 多进程并行执行
        result = runtools.multi_run_tools(tools,shares)
    elif show : # 如果显示dag图，那么也要在执行过程中更新shares中的node状态
        result = runtools.run_tools(tools,shares)
    else:
        result = runtools.run_tools(tools)
    
    print("最终的结果为：")
    base.print_everything(result)
    # 等待show的子进程结束
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
    elif len(errors)>0:
        print(f"经过多轮尝试，仍然存在无法绕过的错误，包括：{errors}")
        print(f"程序结束，请换大语言模型，或者修改任务指令。")
        return []