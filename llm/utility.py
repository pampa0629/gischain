# 把chatglm返回的字符串转换为工具集列表，其他llm返回的字符串是否可用，待验证

def extract_content(string):
    index_left = string.find('[')
    index_right = string.find(']')
    return string[index_left+1:index_right]

def predeal(content:str):
    print(f"大语言模型的返回结果如下：\n{content}")
    content = extract_content(content) # 去掉前后的 []
    
    content = content.replace('\\n', '')
    content = content.replace('\\"', '\"')
    content = content.replace('\\t', '')
    content = content.strip()
    content = content.strip("\"")
    
    tools_str = "[" + content + "]"
    import json
    tool_list = json.loads(tools_str)
    return tool_list

