import json
from tools import define



# 根据用户指令，通过llm在工具集中来初筛工具，返回工具列表
def select_tools(llm, instruction, tools):
    # 构造提示词
    descs = []
    for name in tools:
        print(f"正在筛选工具：{name}")
        desc = define.get_tool_desc(name)
        print(f"工具：{name},描述：{desc}")
        # desc = json.loads(tool_desc)
        # simple = desc["description"]
        descs.append({name:desc})

    prompt = f"""你是GIS领域专家，现在要完成用户指定的任务，指令如下：{instruction}。
    请你根据指令，按照概率从大到小，从工具集中选择可能需要的工具，在中括号[]中用双引号列出工具名即可（如:["abc","def"]）。
    先给出解释，再在[]中输出工具列表；之后，无需给出更多解释，以避免干扰后面程序的读取和运行。记住：可以多选，不要少选。
    工具集如下：{descs}。"""
    print(f"用来刷选工具的提示词为：{prompt}")
    # 传给大模型的提示词，包括用户指令，工具名字和描述，返回工具名字的list
    result_tools = llm.invoke(prompt)
    return result_tools
    # return get_tools_and_example(result_tools, llm.token_len - BASE_TOKEN_LEN)
    
# 通过工具名，得到工具和示例的字符串描述
def get_tools_and_example(names,token_len):
    tokens = 0
    tools = examples = ""
    print("被选择的tool包括: ")
    for name in names:
        if tokens < token_len: # 限制一下token的长度
            tool = json.dumps(define.get_tool_core(name))
            example = define.get_tool_example(name)
            tools += tool
            examples += example
            tool_len = len(tool) + len(example)
            tokens += tool_len
            print(f"工具：{name},字符长度: {tool_len}")
        else:
            print(f"工具：{name} 没有被选择，因为字符长度超过了限制")
    return tools,examples