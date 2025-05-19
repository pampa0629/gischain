# 定义llm必须具备的几个接口：
# set_api_key(key)：设置api_key
# build_prompt(instruction, tools)：构造提示词
# invoke(prompt)：调用大语言模型，返回工具集列表
class Llm:
    def __init__(self):
        # 每个LLM可以自行设定内容输入的token长度
        self.token_len = 8192 

    def set_api_key(self, key):
        pass

    def build_prompt(self, instruction, tools, examples):
        pass

    def invoke(self, text):
        pass

    def invode_with_fc(self, messages, tools):
        pass

