# 参数说明
# instruction: 任务指令
# tools_descs: 工具集描述
# tool_examples: 工具集使用范例，可以设置为""，用来控制token的长度
# is_complex_examples: 是否使用复杂的范例作为输入，用来控制token的长度
# is_output_steps: 是否输出步骤，用来控制输出的token的长度
def build(instruction, tools_descs, tool_examples, is_complex_examples=False,is_output_steps=False):
    if tool_examples != None and tool_examples != "":        
        tool_examples = f"工具集的使用范例如下：【{tool_examples}】"

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
        end += "参考前面的综合范例，按照“观察、想法、行动”的模式，"
    end += "根据下面的任务指令，一步步思考，"
    if is_output_steps:
        end += "先输出分步骤的推理过程，最后再统一"
    end += "输出JSON格式的工具调用，JSON内容放在[]中输出。"
    return end

g_begin = """
你现在是一个GIS领域专家和人工智能助手。现在要做一个GIS领域的空间分析任务，你需要遵从指令完成任务，并满足下面的约束条件的要求。
"""

g_constraint = """
约束条件：
1，从下面的工具集中选择合适的工具，用不上的工具不要选择，也不要自己臆造工具集之外的工具；
2，严格遵从给定的工具集中对工具的能力描述，不要修改其能力，也不要增加或者减少其输入参数；
3，调用工具时的输入数据，要么在任务指令中已经给出，要么是前面工具调用的输出，不要使用没有来源的数据；
4，调用工具后的输出数据，请确保在后续被用上，并且不要在中间步骤就输出最后结果；
5，每个工具都会在说明其输入和输出的数据文件类型，请仔细阅读，并严格遵守对数据类型的要求，记住：tif为栅格文件，shp为矢量文件；
6，输入数据放在data目录下，中间生成的文件放在data/temp目录下，最终结果放在data/output目录下，输出的JSON中一定要组合出完整的文件路径名；
7，请分析任务的内在逻辑，分步骤思考和推理整个过程，保证任务指令中的每一个显性和隐性要求都能达成。
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

g_example1_instruction = """
指令：修一条铁路，宽度为50米，需要计算占用周边的耕地面积。铁路数据是railway.shp,耕地数据是farmland.shp。
"""

# 请参照前面的综合范例，按照“观察、想法、行动”的模式，根据下面的任务指令，分步骤进行思考和推理，并输出分步推理过程和JSON格式的工具调用。

# 步骤1：
# 观察：现在有铁路数据和耕地数据，求宽50米的铁路占用周边耕地的面积
# 想法：我首先要计算出铁路两侧各扩展25米的范围，需要先做缓冲区分析
# 行动：调用buffer工具，输入railway.shp（指令中给出）和25米（指令中给出宽度的一半），输出railway_buffer.shp（在第二步使用）

# 步骤2：
# 观察：现在已经有了宽50米的铁路所占用的范围，以及指令中给出的耕地数据
# 想法：要求铁路范围所占用耕地范围，需要做一个叠加分析
# 行动：调用 overlay 工具，输入railway_buffer.shp（第一步给出）和farmland.shp（指令中给出），输出 overlay.shp（在第三步使用）

# 步骤3：
# 观察：现在已经有了铁路范围与耕地数据的交集，也就是铁路范围会占用的耕地范围
# 想法：要求这个范围的面积，需要做一个求面积的操作
# 行动：调用 area 工具，输入 overlay.shp（第二步给出），输出area_result.json（最终结果）

# 步骤4：
# 观察：现在已经有了面积数据结果area_result.json，指令完成

g_example1_steps = """
步骤1：
观察：现在有铁路数据和耕地数据，求宽50米的铁路占用周边耕地的面积
想法：我首先要计算出铁路两侧各扩展25米的范围，需要先做缓冲区分析
行动：调用buffer工具，输入railway.shp 和25米（宽度的一半），输出railway_buffer.shp

步骤2：
观察：现在已经有了宽50米的铁路所占用的范围，以及指令中给出的耕地数据
想法：要求铁路范围所占用耕地范围，需要做一个叠加分析
行动：调用overlay工具，输入railway_buffer.shp 和 farmland.shp，输出 overlay_result.shp

步骤3：
观察：现在已经有了铁路范围与耕地数据的交集，也就是铁路范围会占用的耕地范围
想法：要求这个范围的面积，需要做一个求面积的操作
行动：调用 area 工具，输入 overlay_result.shp，输出area_result.json

步骤4：
观察：现在已经有了面积数据结果area_result.json，指令完成
"""

g_example1_json = """
json: [
        {
            "name": "buffer",
            "inputs": {
                "datafile": "data/railway.shp",
                "radius": 25
            },
            "output": "data/temp/railway_buffer.shp"
        }, 
        {
            "name": "overlay",
            "inputs": {
                "datafile1": "data/temp/railway_buffer.shp",
                "datafile2": "data/farmland.shp"
            },
            "output": "data/temp/overlay_result.shp"
        },
        {
            "name": "area",
            "inputs": {
                "datafile": "data/temp/overlay_result.shp"
            },
            "output": "data/output/area_result.json"
        }
]
"""

g_example2_instruction = """
指令：修一条铁路，宽度为50米，需要计算占用周边坡度小于10度的耕地面积。铁路数据是railway.shp；耕地数据是farmland.shp；地形数据是terrain.tif。
"""

# 步骤1：
# 观察：指令中提到了地形数据，可用于确定坡度小于10度的区域。
# 想法：首先，需要计算整个区域的坡度情况。
# 行动：调用slope工具，输入terrain.tif（指令中给出），输出为slope.tif（在第2步中使用）。

# 步骤2：
# 观察：现在我们有了一个坡度图层。
# 想法：由于我们只关心坡度小于10度的区域，因此需要从坡度图层中提取这一特定区域。
# 行动：调用extractByValues工具，输入slope.tif（第1步的输出），最小值为0（指令中隐含给出），最大值为10（指令中显性给出），输出 slope_0_10.tif（在第4步中使用）。

# 步骤3：
# 观察：指令要求计算新铁路周围50米宽度范围内的耕地面积。
# 想法：需要先创建一个表示铁路两侧各扩展25米范围的缓冲区。
# 行动：调用buffer工具，输入railway.shp（指令中给出）和25米（指令中给出的宽度的一半），输出 railway_buffer.shp（在第4步中使用）。

# 步骤4：
# 观察：已经有了表示坡度小于10度的区域的栅格数据和铁路缓冲区的矢量数据。
# 想法：需要将坡度小于10度的区域，与 铁路缓冲区做叠加分析，得到 铁路缓冲区范围内、且坡度又小于10度的区域。
# 行动：使用 overlay 工具，输入 slope_0_10.tif（第2步的输出）和railway_buffer.shp（第3步的输出），输出 masked_slope_buffer.tif（在第5步中使用）。

# 步骤5：
# 观察：现在，我们有了坡度小于10度且在铁路缓冲区内的区域的数据，以及耕地数据。
# 想法：接下来，我们需要找出这个区域与耕地的重叠部分。
# 行动：继续使用 overlay 工具，输入 masked_slope_buffer.tif（第4步的输出）和farmland.shp（指令中给出），输出 masked_slope_buffer_farmland.tif（在第6步中使用）。

# 步骤6：
# 观察：我们现在得到了一个文件，它包含了坡度小于10度的耕地和铁路缓冲区的交集。
# 想法：为了回答初始问题，我们需要计算这个交集区域的面积。
# 行动：调用 area 工具，输入 masked_slope_buffer_farmland.tif（第5步的输出），输出 area_result.json（最终结果）。

# 步骤7：
# 观察：现在已经有了面积数据结果 area_result.json，指令完成

g_example2_steps = """
步骤1：
观察：指令中提到了地形数据，可用于确定坡度小于10度的区域。
想法：首先，需要计算整个区域的坡度情况。
行动：调用slope工具，输入terrain.tif，输出为slope.tif。

步骤2：
观察：现在我们有了一个坡度图层。
想法：由于我们只关心坡度小于10度的区域，因此需要从坡度图层中提取这一特定区域。
行动：调用extractByValues工具，输入slope.tif，最小值为0，最大值为10，输出 slope_0_10.tif。

步骤3：
观察：指令要求计算新铁路周围50米宽度范围内的耕地面积。
想法：需要先创建一个表示铁路两侧各扩展25米范围的缓冲区。
行动：调用buffer工具，输入railway.shp和25米（宽度的一半），输出 railway_buffer.shp。

步骤4：
观察：已经有了表示坡度小于10度的区域的栅格数据和铁路缓冲区的矢量数据。
想法：需要将坡度小于10度的区域，与 铁路缓冲区做叠加分析，得到 铁路缓冲区范围内、且坡度又小于10度的区域。
行动：使用 overlay 工具，输入 slope_0_10.tif和railway_buffer.shp，输出 masked_slope_buffer.tif。

步骤5：
观察：现在，我们有了坡度小于10度且在铁路缓冲区内的区域的数据，以及耕地数据。
想法：接下来，我们需要找出这个区域与耕地的重叠部分。
行动：继续使用 overlay 工具，输入 masked_slope_buffer.tif和farmland.shp，输出 masked_slope_buffer_farmland.tif。

步骤6：
观察：我们现在得到了一个文件，它包含了坡度小于10度的耕地和铁路缓冲区的交集。
想法：为了回答初始问题，我们需要计算这个交集区域的面积。
行动：调用 area 工具，输入 masked_slope_buffer_farmland.tif，输出 area_result.json。

步骤7：
观察：现在已经有了面积数据结果 area_result.json，指令完成
"""

g_example2_json = """
json: 
[
    {
        "name": "slope",
        "inputs": {
            "tiffile": "data/terrain.tif"
        },
        "output": "data/temp/slope.tif"
    },
    {
        "name": "extractByValues",
        "inputs": {
            "tiffile": "data/temp/slope.tif",
            "min": 0,
            "max": 10
        },
        "output": "data/temp/slope_0_10.tif"
    },
    {
        "name": "buffer",
        "inputs": {
            "datafile": "data/railway.shp",
            "radius": 25
        },
        "output": "data/temp/railway_buffer.shp"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/slope_0_10.tif",
            "datafile2": "data/temp/railway_buffer.shp"
        },
        "output": "data/temp/overlay_slope_railway.tif"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/overlay_slope_railway.tif",
            "datafile2": "data/farmland.shp"
        },
        "output": "data/temp/overlay_slope_railway_farmland.tif"
    },    
    {
        "name": "area",
        "inputs": {
            "datafile": "data/temp/overlay_slope_railway_farmland.tif"
        },
        "output": "data/output/area_result.json"
    }
]
"""