from .prompt_examples import g_example1_instruction,g_example1_steps,g_example1_json
from .prompt_examples import g_example2_instruction,g_example2_steps,g_example2_json

# 参数说明
# instruction: 任务指令
# tools_descs: 工具集描述
# tool_examples: 工具集使用范例，可以设置为""，用来控制token的长度
# is_complex_examples: 是否使用复杂的范例作为输入，用来控制token的长度
# is_output_steps: 是否输出步骤，用来控制输出的token的长度
def build(instruction, tools_descs, tool_examples, is_complex_examples=False,is_output_steps=False):
    if tool_examples != None and tool_examples != "":        
        tool_examples = f"工具集的使用举例如下：“““{tool_examples}”””"

    complex_examples = ""
    if is_complex_examples:
        complex_examples = f"""综合范例如下：【{g_example1_instruction}{g_example1_steps}{g_example1_json}
                                            {g_example2_instruction}{g_example2_steps}{g_example2_json}】"""
    
    end = build_end(is_complex_examples,is_output_steps)
    
    text  = g_template.format(begin=g_begin,constraint=g_constraint,
                            tools=tools_descs, tool_examples=tool_examples,
                            complex_examples = complex_examples,
                            end=end, instruction=instruction,)
    print(f"输入给大语言模型的内容如下:{text}")
    return text

# 结束词比较复杂，要单独构造
def build_end(is_complex_examples,is_output_steps):
    end = "请"
    if is_complex_examples:
        end += "参考前面的综合范例，按照“思考、行动、观察”的模式，"
    end += "一步步推理，完成下面的任务指令，"
    if is_output_steps:
        end += "先输出分步骤的推理过程，最后再统一"
    else:
        end += "无须输出推理过程，直接"
    end += "输出JSON格式的工具调用，JSON内容放在[]中输出。"
    return end

g_begin = """
你现在是一个GIS领域专家和人工智能助手。现在要做一个GIS领域的空间分析任务，你需要遵从指令完成任务，并满足下面的约束条件的要求。
"""

g_constraint = """约束条件：
1，从下面的工具集中选择合适的工具，用不上的工具不要选择，也不要自己臆造工具集之外的工具；非GIS类工具，只要有可能用上且在工具集中，也要选用；
2，严格遵从给定的工具集中对工具的能力描述，不要修改其能力，也不要增加或者减少其输入参数；
3，调用工具时的输入数据，要么在任务指令中已经给出，要么是前面工具调用的输出，不要使用没有来源的数据；
4，调用工具后的输出数据，请确保在后续被用上，并且不要在中间步骤就输出最后结果；
5，每个工具都会在说明其输入和输出的数据文件类型，请仔细阅读，并严格遵守对数据类型的要求，记住：tif为栅格文件，shp为矢量文件；
6，输入数据放在data目录下，中间生成的文件放在data/temp目录下，最终结果放在data/output目录下，输出的JSON中一定要组合出完整的文件路径名；
7，请认真分析任务的内在逻辑，一步步思考和推理，保证任务指令中的每一个显性和隐性要求都能达成。
"""

g_template = """
{begin}
{constraint}
工具集如下：
[{tools}
]
{tool_examples}
{complex_examples}
{end}
任务指令：{instruction}
"""

g_fc_system= """
You are a friendly chatbot that can use external tools to offer reliable assistance to human beings. 
"""

g_fc_attention = """
约束条件：
1，输出的tools中，arguments的output参数必须提供出来，不能省略。请注意输入参数和输出参数要严格对应，避免错别字；
2，输入的数据文件名字一定要严格遵从给出的数据json描述，不要翻译为英文；也不要自行给数据文件添加不存在的新目录。
3，原始数据文件放在./data目录下，中间生成的文件放在./data/temp目录下，最终结果放在./data/output目录下；
4，tools调用的参数中一定要组合出完整的文件路径名，避免工具实际执行时找不到对应的数据文件。
"""