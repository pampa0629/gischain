from llm.chatglm import ChatGLM
from llm.qwen import QWen

def init_llm(name, key=None):
    if name == "chatglm":
        if key == None:
            raise Exception("chatglm需要一个key")
        from llm import chatglm
        chatglm = ChatGLM()
        chatglm.set_api_key(key)
        return chatglm
    elif name == "qwen-turbo":
        if key == None:
            raise Exception("qwen-turbo需要一个key")
        from llm import qwen
        qwen = QWen()
        qwen.set_api_key(key)
        return qwen
    else:
        raise Exception("不支持的llm:"+ name)