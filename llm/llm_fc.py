# 支持openai接口的function call的大模型对象

from openai import OpenAI
from .llm import Llm
from .prompt_template import g_fc_system,g_fc_attention

class Llm_fc(Llm):
    def __init__(self, name, key):
        base_url = ""
        # 如果名字中包括qwen
        if name.find("qwen") != -1:
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 填写DashScope SDK的base_url
        elif name.find("ollama") != -1 :
            base_url="http://localhost:11434/v1"
        elif name.find("gpt") != -1 :
            base_url="https://api.openai-proxy.org/v1"
        else:
            print("模型:{name}尚不支持function call")
            
        self.client = OpenAI(
            api_key=key,
            base_url=base_url
        )
        self.model=name

    def build_prompt(self, instruction, tools, examples):
        return [
            {"role": "system", "content": g_fc_system},
            {"role": "user", "content": instruction+g_fc_attention}
        ]

    def invode_with_fc(self, messages, tools):
        print("invode_with_fc:", messages, tools)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        return completion

    def invoke(self, text, tools=None, errors=None):
        messages=[{"role": "system", "content": "You are a GIS domain expert and a helpful assistant."},
                      {"role": "user", "content": text}]
        if tools!=None:
            messages+=[{'role': 'assistant', 'content': tools}]
        if errors!=None:
            messages+=[{'role': 'user', 'content': errors}]
        # response = openai.ChatCompletion.create(
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.01)
        content = response.choices[0].message.content
        print("llm fc's response：", content,"\n")
        from .base import predeal
        return predeal(content)