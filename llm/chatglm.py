import zhipuai

# prompt = """
# 你现在是一个人工智能助手，现在要做一个gis领域的空间分析功能。
# 你需要遵从指令完成特定的任务，从下面工具集中选择合适的工具(不要选用不上的工具)，
# 并用JSON格式顺序列出对应的工具，请给出对应的输入信息，记得组合出完整的文件路径名。
# 由于要对接程序自动运行，不要有任何多余的文字输出，多余的文字都是干扰项。
# 指令：{instruction}
# 工具集如下：
# ==========
# {tools}
# ==========
# """

def set_api_key(key):
    zhipuai.api_key = key

def invoke_llm(text):
    response = zhipuai.model_api.invoke(
        model="chatglm_pro", #  chatglm_std  chatglm_pro
        prompt=[{"role": "user", "content": text}],
        top_p=0.7,
        temperature=0.01,
    )
    content = response['data']['choices'][0]['content']
    from . import utility
    return utility.predeal(content)
    