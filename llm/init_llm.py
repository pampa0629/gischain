
def init_llm(name, key=None):
    if key == None:
            raise Exception("调用在线大语言模型需要一个key，请到对应的网站申请")
    
    if name == "chatglm":
        from llm import chatglm
        allm = chatglm.ChatGLM()
    elif name == "qwen-turbo":
        from llm import qwen
        allm = qwen.QWen()
    elif name == "ErnieBot":
        from llm import erniebot
        allm = erniebot.ErnieBot()
    elif name == "gpt4":
        from llm import gpt4
        allm = gpt4.GPT4()
    else:
        raise Exception("不支持的llm:"+ name)
    
    allm.set_api_key(key)
    return allm