# 检查大模型返回的json，是否存在逻辑上的问题，如果存在，把问题发给大模型重新生成

from tools import define

# 检查工具在中间生成的临时数据，后面的工具是否都能用到
def check_use_temp_data(tools):
    temps_used = {} # {"buffer.shp":{tool:"buffer",used:False}}
    # 先把所有的中间数据都放到temps_used中，统一记录为没有使用过
    for index, tool in enumerate(tools):
        if index < len(tools) - 1: # 要跳过最后一个工具的输出
            temps_used[tool['parameters']['output']] = {'tool':tool['name'], 'used':False}
    # 再遍历一遍，把中间数据的使用情况记录下来
    for tool in tools:
        for input in tool['parameters']['inputs'].values():
            if isinstance(input, list)==False and input in temps_used:
                temps_used[input]['used'] = True
    
    # 最后记录下来所有仍然没有被使用过的中间数据
    errors = ""
    for temp, data in temps_used.items():
        if data['used'] == False:
            errors += f"工具 {data['tool']} 输出的中间数据 {temp} 没有被后面的工具使用过，要么不应调用该工具，要么生成的数据应该被后面所使用；"
    
    return len(errors) == 0, errors

# 检查第一个工具的调用，输入的文件是否存在
def check_first_input_file(tools):
    import os
    tool = tools[0]
    for key, value in tool['parameters'].items():
        if "file" in key and key!='output' and os.path.exists(value) == False:
            return False, f"文件{value}没有在指定的位置，请根据要求组合好正确的数据目录；"
    return True, ""

# 判断一个字符串是否属于一个list中某个字符串的一部分
def find_in_list(str, list):
    for item in list:
        if str in item:
            return True
    return False

# 检查所有的数据文件输入，在指令中或者前面的工具输出中是否存在
def check_input_file(tools, instruction, data_descs):
    import os, json
    # 从 data_descs 中得到 files
    data = json.loads("["+data_descs+"]")
    files = [list(item.keys())[0] for item in data]
    print(f"check中，所有的files为：{files}")

    for tool in tools:
        for key, value in tool['parameters'].items():
            if "file" in key:
                if find_in_list(os.path.basename(value),files)==False:
                    return False, f"工具 {tool['name']} 的输入文件 {value} 无法确定来源，不要自己臆造数据文件；"
        files.append(tool['parameters']['output']) # 把工具的输出也加入到文件列表中
    return True, ""

# 根据大模型返回的工具列表，检查是否存在可能的错误。若存在错误，则返回False和检查出来的所有错误信息
def check_tools(tools, instruction, data_descs):
    errors = ""
    # 用每个工具自己带的check函数检查一遍
    for tool in tools:
        ok, error = define.check_tool(tool['name'], tool)
        if ok == False:
            errors += error

    # 检查工具在中间生成的临时数据，后面的工具是否都能用到
    ok, error = check_use_temp_data(tools)
    if ok == False:
        errors += error

    # 检查所有的数据文件输入，在指令中或者前面的工具输出中是否存在
    ok, error = check_input_file(tools, instruction, data_descs)
    if ok == False:
        errors += error

    # 检查第一个工具的调用，输入的文件是否存在
    ok, error = check_first_input_file(tools)
    if ok == False:
        errors += error

    if len(errors) > 0:
        errors = f"发现以下错误：{errors}。请纠正后一次性输出完整json结果。"
        return False, errors
    return True, errors