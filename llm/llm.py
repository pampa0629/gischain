# 定义llm必须具备的几个接口：
# set_api_key(key)：设置api_key
# build_prompt(instruction, tools)：构造提示词
# invoke(prompt)：调用大语言模型，返回工具集列表
class Llm:
    # def __init__(self):
    #     pass

    def set_api_key(self, key):
        pass

    def build_prompt(self, instruction, tools):
        pass

    def invoke(self, text):
        pass

