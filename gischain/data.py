import json
from llm.base import extract_content

# 从统一的元数据描述文件中读取数据文本
def load_meta(metafile):
    with open(metafile,'r', encoding='utf-8') as f:
        return f.read()

# 从json格式的数据描述中选取指定名称的数据
def get_data_items(data, names):
    result = []
    for name in names:
        if name in data:
            result.append({name:data[name]})
    return result

# 通过大模型，根据任务指令，刷选出需要的数据，用文字描述返回结果
def select_data(llm, instruction):
    meta = load_meta("data/data.meta")
    # print(f"元数据描述为：{meta}")
    prompt = f"""你是GIS领域专家，现在要完成用户指定的任务，指令如下：“{instruction}”。
    请你根据指令，按照概率从大到小，从下面的数据集中选择可能需要的数据，先给出解释，最后在中括号[]中用双引号列出数据名即可（如:["abc","def"]）。
    在[]的后面，不要再有任何输出，以避免干扰后面的程序执行。肯定不会被用到的数据不要列出。
    数据集如下：[{meta}]。"""
    print(f"用来选择数据的提示词为：{prompt}")
    # 传给大模型的提示词，包括用户指令，元数据描述，返回数据名字的list
    names = llm.invoke(prompt)      

    json_meta = json.loads(meta)  
    # print(f"元数据的json格式为：{json_meta}")
    # 从json格式的数据描述中选取指定名称的数据
    items = get_data_items(json_meta, names)
    # print(f"选择的数据items的json内容为：{items}")
    # 返回数据的文字描述
    text = json.dumps(items, ensure_ascii=False)
    # print(f"输出为文本内容：{text}")
    return extract_content(text)