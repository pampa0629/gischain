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

g_constraint = """
约束条件：
1，从下面的工具集中选择合适的工具，用不上的工具不要选择，也不要自己臆造工具集之外的工具；
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

g_example1_instruction = """
指令：修一条铁路，宽度为50米，需要计算占用周边的耕地面积。铁路数据是railway.shp,耕地数据是farmland.shp。
"""

g_example1_steps = """
步骤1：
思考：要计算一定宽度的铁路占用耕地的面积，首先要计算出铁路所占范围来，那么应该做缓冲区分析
行动：调用buffer工具，输入railway.shp 和25米（宽度的一半），输出railway_buffer.shp
观察：现在已经有了带宽度的铁路所占用的范围，以及指令中给出的耕地数据

步骤2：
思考：要求带宽度的铁路范围所占用耕地范围，需要对这两个数据做一个叠加分析
行动：调用overlay工具，输入railway_buffer.shp 和 farmland.shp，输出 overlay_result.shp
观察：现在已经有了铁路范围与耕地数据的交集，也就是铁路范围会占用的耕地范围

步骤3：
思考：要求这个范围的面积，需要做一个求面积的操作
行动：调用 area 工具，输入 overlay_result.shp，输出area_result.json
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

g_example2_steps = """
步骤1：
思考：要计算占用周边坡度小于10度的耕地面积，首先要计算出坡度小于10度的区域来，那么应该做坡度分析。
行动：调用slope工具，输入terrain.tif，输出为slope.tif。
观察：现在已经有了一个坡度图层。

步骤2：
思考：要计算坡度小于10度的区域，需要对坡度图层做一个提取分析。
行动：调用extractByValues工具，输入slope.tif，最小值为0，最大值为10，输出 slope_0_10.tif。
观察：现在已经有了坡度小于10度的区域。

步骤3：
思考：已经有了坡度小于10度的区域，那么就可以计算在这里范围内的耕地面积。
行动：调用overlay工具，输入slope_0_10.tif和farmland.shp，输出 overlay_slope_farmland.tif。
观察：现在已经有了坡度小于10度的区域和耕地数据的交集。

步骤4：
思考：接下来，我们需要找出这个区域与铁路的重叠部分。但原始的铁路数据是线状的，需要先创建一个表示铁路两侧各扩展25米范围的缓冲区。
行动：调用buffer工具，输入railway.shp和25米（宽度的一半），输出 railway_buffer.shp。
观察：现在已经有了表示铁路两侧各扩展25米范围的缓冲区。

步骤5：
思考：接下来，我们需要找出“坡度小于10度的区域和耕地数据的交集”与铁路缓冲区的重叠部分。
行动：继续使用 overlay 工具，输入 overlay_slope_farmland.tif和railway_buffer.shp，输出 overlay_slope_farmland_buffer.tif。
观察：现在已经有了坡度小于10度的耕地且在铁路缓冲区内的区域的数据。

步骤6：
思考：为了回答初始问题，我们需要计算这个交集区域的面积。
行动：调用 area 工具，输入 masked_slope_buffer_farmland.tif，输出 area_result.json。
观察：现在已经有了面积数据结果 area_result.json，指令完成。
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
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/slope_0_10.tif",
            "datafile2": "data/temp/farmland.shp"
        },
        "output": "data/temp/overlay_slope_farmland.tif"
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
            "datafile1": "data/temp/overlay_slope_farmland.tif",
            "datafile2": "data/railway_buffer.shp"
        },
        "output": "data/temp/overlay_slope_farmland_buffer.tif.tif"
    },    
    {
        "name": "area",
        "inputs": {
            "datafile": "data/temp/overlay_slope_farmland_buffer.tif.tif"
        },
        "output": "data/output/area_result.json"
    }
]
"""