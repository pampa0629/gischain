# 一些LLM中需要用到的基础函数

# 从一对符号中提取内容
def extract_content(string, left='[', right=']'):
    index_left = string.rfind(left)
    index_right = string.rfind(right)
    return string[index_left+1:index_right]

# 把LLM返回的字符串转换为工具集列表
def predeal(content):
    print(f"大语言模型的返回结果如下：\n{content}")
    content = extract_content(content) # 去掉前后的 []
    tools_str = "[" + content + "]"
    import json
    tool_list = json.loads(tools_str)
    return tool_list