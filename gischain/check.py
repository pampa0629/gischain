# 检查大模型返回的json，是否存在逻辑上的问题，如果存在，把问题发给大模型重新生成

import json
from tools import define

# 把旧版的 inputs/output 顶层格式，归一化为 parameters 格式（原地修改）
# 背景：v0.1.6 引入 function call 后，运行时统一采用 parameters 格式；
# 但历史版本和部分 few-shot 范例存在多种格式，大模型可能照着输出，这里统一做兼容：
#   旧格式1（v0.1.7及以前）：{"name":..., "inputs":{...}, "output":"..."}
#   旧格式2（v0.1.8迁移残留）：{"name":..., "parameters":{"inputs":{...}, "output":"..."}}
#   规范格式（当前）：{"name":..., "parameters":{参数1:..., 参数2:..., "output":"..."}}
def normalize_tool(tool):
    if isinstance(tool, dict) == False:
        return tool
    if "parameters" not in tool:
        inputs = tool.get("inputs")
        params = dict(inputs) if isinstance(inputs, dict) else {}
        if "output" in tool: # 旧格式的output在顶层
            params["output"] = tool.pop("output")
        tool["parameters"] = params
    elif isinstance(tool["parameters"], dict) and isinstance(tool["parameters"].get("inputs"), dict):
        # 旧格式2：parameters下嵌套inputs和output
        params = dict(tool["parameters"]["inputs"])
        if "output" in tool["parameters"]:
            params["output"] = tool["parameters"]["output"]
        tool["parameters"] = params
    elif "output" in tool and "output" not in tool["parameters"]:
        # 混合格式：output在顶层，其余参数在parameters中
        tool["parameters"]["output"] = tool.pop("output")
    tool.pop("inputs", None) # 旧格式字段清理
    return tool

# 检查工具在中间生成的临时数据，后面的工具是否都能用到
def check_use_temp_data(tools):
    temps_used = {} # {"buffer.shp":{tool:"buffer",used:False}}
    # 先把所有的中间数据都放到temps_used中，统一记录为没有使用过
    for index, tool in enumerate(tools):
        if index < len(tools) - 1: # 要跳过最后一个工具的输出
            output = tool['parameters']['output']
            if isinstance(output, str): # 防御：output不是字符串时无法作为文件名追踪
                temps_used[output] = {'tool':tool['name'], 'used':False}
    # 再遍历一遍，把中间数据的使用情况记录下来
    for tool in tools:
        inputs = {key: value for key, value in tool["parameters"].items() if key != "output"}
        for input in inputs.values():
            if isinstance(input, str) and input in temps_used:
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
        if "file" in key and key != 'output' and isinstance(value, str) and os.path.exists(value) == False:
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
    import os
    # 从 data_descs 中得到 files；解析失败不致命，按空数据处理
    try:
        data = json.loads("[" + (data_descs or "") + "]")
        files = [list(item.keys())[0] for item in data if isinstance(item, dict) and len(item) > 0]
    except Exception as e:
        print(f"check_input_file 解析数据描述失败：{e}")
        files = []
    print(f"check中，所有的files为：{files}")

    for tool in tools:
        for key, value in tool['parameters'].items():
            if "file" in key and isinstance(value, str):
                if find_in_list(os.path.basename(value), files) == False:
                    return False, f"工具 {tool['name']} 的输入文件 {value} 无法确定来源，不要自己臆造数据文件；"
        files.append(tool['parameters']['output']) # 把工具的输出也加入到文件列表中
    return True, ""

# 根据大模型返回的工具列表，检查是否存在可能的错误。若存在错误，则返回False和检查出来的所有错误信息
def check_tools(tools, instruction, data_descs):
    # 防御：大模型调用失败（返回None）或返回了异常结构
    if tools is None or isinstance(tools, list) == False or len(tools) == 0:
        return False, "大语言模型没有返回有效的工具调用列表，请重新输出JSON格式的工具调用，JSON内容放在[]中；"

    # 先做格式归一化：旧版inputs/output顶层格式 -> parameters格式（原地修改，后续执行直接受益）
    for tool in tools:
        normalize_tool(tool)

    errors = ""
    # 检查每个工具调用的结构是否完整（name、parameters、output缺一不可）
    valid_tools = []
    for tool in tools:
        if isinstance(tool, dict) and "name" in tool and isinstance(tool.get("parameters"), dict) and "output" in tool["parameters"]:
            valid_tools.append(tool)
        else:
            errors += f"工具调用{json.dumps(tool, ensure_ascii=False)}的结构不完整，缺少name、parameters或output字段；"
    if len(valid_tools) == 0:
        return False, errors + "请严格遵从工具集的格式要求输出；"

    # 用每个工具自己带的check函数检查一遍
    for tool in valid_tools:
        ok, error = define.check_tool(tool['name'], tool)
        if ok == False:
            errors += error

    # 检查工具在中间生成的临时数据，后面的工具是否都能用到
    ok, error = check_use_temp_data(valid_tools)
    if ok == False:
        errors += error

    # 检查所有的数据文件输入，在指令中或者前面的工具输出中是否存在
    ok, error = check_input_file(valid_tools, instruction, data_descs)
    if ok == False:
        errors += error

    # 检查第一个工具的调用，输入的文件是否存在
    ok, error = check_first_input_file(valid_tools)
    if ok == False:
        errors += error

    if len(errors) > 0:
        errors = f"发现以下错误：{errors}。请纠正后一次性输出完整json结果。"
        return False, errors
    return True, errors
