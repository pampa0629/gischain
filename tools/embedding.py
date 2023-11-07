import numpy as np

# ========  通用向量化工具 ======================== #
import os

# 通义千问的向量化
def tongyi_emb(text):
    import dashscope
    dashscope.api_key=os.environ.get("qwen_key")
    resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v1,
        input=text)
    return resp["output"]["embeddings"][0]["embedding"]

# openai 的向量化
def openai_text2em(text):
    import openai
    openai.api_base = 'https://api.closeai-asia.com/v1' # 固定不变
    openai.api_key = os.environ.get("gpt_key")
    result = openai.Embedding.create(
                    model="text-embedding-ada-002",
                    input=text
                )
    emb = result["data"][0]["embedding"] 
    emb = [float(x) for x in emb]
    return emb

# baidu 的向量化
import requests
import json
def baidu_em(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=" + get_access_token()
    payload = json.dumps({
        "input": [
            text
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    emb = response["data"][0]["embedding"] 
    emb = [float(x) for x in emb]
    return emb
    
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", 
              "client_id":os.environ.get("wenxin_ak"), 
              "client_secret": os.environ.get("wenxin_sk") }
    return str(requests.post(url, params=params).json().get("access_token"))

# ============ 工具的向量化、存储和加载 =========================================== #

# 加载工具的字符串向量值
def load_tools_emb():
    # 先看看有没有json缓存文件
    import os
    if os.path.exists("tools_emb.json"):
        import json
        with open("./tools/tools_emb.json", "r", encoding="utf-8") as f:
            tools_emb = json.load(f)
    else:    
        # 找不到就重新计算
        from . import define
        tools = define.get_tools_name()
        tools_emb = [{"tool":tool,"emb":tongyi_emb(define.get_tool_desc(tool)+define.get_tool_example(tool))} for tool in tools]
    
    # 然后再保存起来
    import json
    with open("./tools/tools_emb.json", "w", encoding="utf-8") as f:
        json.dump({emb["tool"]:emb["emb"] for emb in tools_emb}, f)

    # 这里还要转为numpy数组
    tools_emb = [{"tool":emb["tool"],"emb":np.array(emb["emb"])} for emb in tools_emb]    
    return tools_emb


# 计算余弦相似度，越大越近似
def cos_simily(data1, data2):
    result = np.dot(data1, data2) / (np.linalg.norm(data1) * np.linalg.norm(data2))
    return result

# 计算欧几里德距离，越小越近似
def ou_simily(data1, data2):
    result = np.linalg.norm(data1 - data2)
    return result

# 计算曼哈顿距离，越小越近似
def man_simily(data1, data2):
    result = np.sum(np.abs(data1 - data2))
    return result

# 计算综合指标，越小越近似
def calc_CI(data1, data2):
    c = cos_simily(data1, data2)
    o = ou_simily(data1, data2)
    m = man_simily(data1, data2)
    return o*m/c/10000.0

# 对tools进行向量相似度综合指标的排序，从小到大
def sort_tools_by_CI(embs,input):
    for emb in embs:
        emb["CI"] = calc_CI(input,emb["emb"])
    embs = sorted(embs, key=lambda x: x["CI"])
    return embs

# ============  通过向量来选择需要的工具 =========================================== #
import tools.define as define

# 根据用户指令，通过向量化来选择工具集
def select_tools(instruction, tools, token_len=4096):
    from tools import embedding
    import numpy as np
    input = np.array(embedding.tongyi_emb(instruction))
    embs = define.get_tools_emb(tools)
    sorted_embs = embedding.sort_tools_by_CI(embs, input)
    descs = examples = ""
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