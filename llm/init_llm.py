
def init_llm(name, key=None, funcall=False):
    if key == None:
            raise Exception("调用在线大语言模型需要一个key，请到对应的网站申请")
    
    if funcall: # 特殊对待
        from llm import llm_fc
        allm = llm_fc.Llm_fc(name,key)
    elif name == "chatglm":
        from llm import chatglm
        allm = chatglm.ChatGLM()
    elif name == "qwen-turbo":
        from llm import qwen
        allm = qwen.QWen()
    elif name == "deepseek":
        from llm import deepseek
        allm = deepseek.Deepseek()
    elif name == "ErnieBot4":
        from llm import erniebot
        allm = erniebot.ErnieBot()
    elif name == "gpt3.5":
        from llm import gpt3_5
        allm = gpt3_5.GPT3_5()
    elif name == "gpt4":
        from llm import gpt4
        allm = gpt4.GPT4()
    elif name == "text2sql":
        from llm import text2sql
        allm = text2sql.Text2SQL()
    else:
        raise Exception("不支持的llm:"+ name)
    
    allm.set_api_key(key)
    return allm