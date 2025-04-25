import json
from tools import define

BASE_TOKEN_LEN = 500 # 基础的token长度

# 根据用户指令，通过llm在工具集中来初筛工具，返回工具描述和示例
def select_tools(llm, instruction, tools):
    # 构造提示词
    simples = []
    for name in tools:
        print(f"正在筛选工具：{name}")
        desc = json.loads(define.get_tool_desc(name))
        simple = desc["description"]
        simples.append({name:simple})

    prompt = f"""你是GIS领域专家，现在要完成用户指定的任务，指令如下：{instruction}。
    请你根据指令，按照概率从大到小，从工具集中选择可能需要的工具，在中括号[]中用双引号列出工具名即可（如:["abc","def"]）。
    先给出解释，再在[]中输出工具列表；之后，无需给出更多解释，以避免干扰后面程序的读取和运行。记住：可以多选，不要少选。
    工具集如下：{simples}。"""
    print(f"用来刷选工具的提示词为：{prompt}")
    # 传给大模型的提示词，包括用户指令，工具名字和描述，返回工具名字的list
    result_tools = llm.invoke(prompt)        
    return get_tools_desc_example(result_tools, llm.token_len - BASE_TOKEN_LEN)
    
# 通过工具名，得到工具描述和示例
def get_tools_desc_example(names,token_len):
    tokens = 0
    descs = examples = ""
    print("被选择的tool包括: ")
    for name in names:
        if tokens < token_len: # 限制一下token的长度
            desc = define.get_tool_desc(name)
            example = define.get_tool_example(name)
            descs += desc
            examples += example
            tool_len = len(desc) + len(example)
            tokens += tool_len
            print(f"工具：{name},字符长度: {tool_len}")
        else:
            print(f"工具：{name} 没有被选择，因为字符长度超过了限制")
    return descs,examples