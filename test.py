prompt = """
指令：{instruction}
工具集如下：
==========
{tools}
==========
"""

instruction = "hello"
tools = "gistools"
prompt  = prompt.format(instruction=instruction,tools=tools)
print(prompt)