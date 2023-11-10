text3 = """
你现在是一个GIS领域专家和人工智能助手。现在要做一个GIS领域的空间分析任务，你需要遵从指令完成任务，并满足下面的约束条件的要求。

约束条件：
1，从下面的工具集中选择合适的工具，用不上的工具不要选择，也不要自己臆造工具集之外的工具；
2，每个工具都会在说明其输入和输出的数据文件类型，请仔细阅读，并严格遵守对数据类型的要求，记住：tif为栅格文件，shp为矢量文件；
3，请认真分析任务的内在逻辑，一步步思考和推理，保证任务指令中的每一个显性和隐性要求都能达成。

工具集如下：
[
{
"name":"buffer",
"description":"得到缓冲区",
"inputs":{
"datafile":"要求缓冲区的数据文件",
"radius":"缓冲区半径"
},
"output":"缓冲区结果文件"
}

{
"name":"slope",
"description":"根据地形数据计算坡度",
"inputs":{
"tiffile":"栅格地形tiff文件"
},
"output":"坡度计算结果的栅格tiff文件"
}

{
"name":"area",
"description":"求面积；如果输入是矢量文件，则求所有要素的面积和；如果输入是栅格文件，则求所有非nodata像元的面积和",
"inputs":{
"datafile":"要求面积的数据文件"
},
"output":"面积结果"
}

{
"name":"overlay",
"description":"叠加分析;支持矢量与矢量、矢量与栅格、栅格与栅格的叠加分析;如果两个输入文件都是矢量，则结果为矢量文件；如果两个输入文件一个为栅格、另一个为矢量，则结果为栅格文件（tif格式）；如果两个输入文件都是栅格，则结果也为栅格文件；目前仅支持intersection模式",
"inputs":{
"datafile1":"参与叠加分析的数据文件1",
"datafile2":"参与叠加分析的数据文件2"
},
"output":"叠加分析结果文件"
}

{
"name":"extractByValues",
"description":"根据给定的最小最大值提取栅格数据，对最小最大值范围之外的像元赋值为NoData",
"inputs":{
"tiffile":"被提取的栅格tiff文件",
"min":"最小值",
"max":"最大值"
},
"output":"提取后的栅格tiff文件"
}

{
"name":"rasterStatistics",
"description":"根据矢量面要素内的有效栅格值计算统计量，包括像元个数、像元面积和等，统计值输出到矢量面要素属性表中",
"inputs":{
"tiffile":"要被统计的栅格tiff文件",
"shpfile":"用来进行统计的矢量面要素文件",
"mode":"统计模式，包括count（像元个数）、area（像元面积和）等",
"field":"统计结果输出到矢量面要素属性表中的字段名"
},
"output":"输出的带统计结果的矢量面要素文件，一般就是输入的shpfile",
}

{
"name":"grouptatistics",
"description":"分组统计功能，根据分组字段对每个组内的数据进行统计",
"inputs":{
"datafile":"要进行分组统计的矢量数据文件",
"field":"要统计数据的字段名",
"mode":"统计模式，包括count（个数）、sum（求和）等",
"group by":"进行分组统计的字段名"
},
"output":"输出的带统计结果的矢量面要素文件，一般就是输入的shpfile",
}

{
"name":"sort",
"description":"根据指定字段的属性值进行排序",
"inputs":{
"datafile":"要进行排序的矢量数据文件",
"field":"要进行排序的字段名",
"mode":"排序方式，包括asc（升序）、desc（降序）等"
},
"output":"输出的排序后的矢量面要素文件，一般就是输入的文件",
}

]

请根据下面的任务指令，一步步推理，输出JSON格式的工具调用，JSON内容放在[]中输出。
任务指令：修一条铁路，宽度为50米，需要分组统计所占用周边坡度小于10度、海拔小于100米、各县区的耕地面积，并汇总到所属地区，从大到小的顺序进行排序。
铁路数据是railway.shp；耕地数据是farmland.shp,地区字段名为"City"，县区字段名为“County”；地形数据是terrain.tif。
"""

text = """
You are now an expert in the GIS field and an AI assistant. 
Answer the following questions as best you can. 
You have access to the following tools:
[
    {
        "name": "buffer",
        "description": "Get a buffer",
        "inputs": {
            "datafile": "Data file requiring a buffer",
            "radius": "Buffer radius"
        },
        "output": "Buffer result file"
    },
    {
        "name": "slope",
        "description": "Calculate slope based on terrain data",
        "inputs": {
            "tiffile": "Raster terrain TIFF file"
        },
        "output": "Raster TIFF file with slope calculation results"
    },
    {
        "name": "area",
        "description": "Calculate area",
        "inputs": {
            "datafile": "Data file requiring area calculation"
        },
        "output": "Area calculation result"
    },
    {
        "name": "overlay",
        "description": "Overlay analysis",
        "inputs": {
            "datafile1": "Data file 1",
            "datafile2": "Data file 2"
        },
        "output": "Overlay analysis result file"
    },
    {
        "name": "extractByValues",
        "description": "Extract raster data based on given minimum and maximum values",
        "inputs": {
            "tiffile": "Raster TIFF file to be extracted",
            "min": "Minimum value",
            "max": "Maximum value"
        },
        "output": "Extracted raster TIFF file"
    }
]

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of  upper tool names, using the following json format.
{
	name: used tool name,
	inputs:{
		used inputs file or value
	},
	output: output file or value
}
Observation: the result of the action, same as the output of the tool
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Please only provide the Thought, Action and Observation of the next step with selecting one tool, do not provide subsequent steps.
Question: To construct a railway with a width of 30 meters, calculate the area of farmland that has slopes of less than 15 degrees in the vicinity. The railway data is in 'railway.shp,' the farmland data is in 'farmland.shp,' and the terrain data is in 'terrain.tif. 

Thought: 
"""
# Based on the following task instruction, think comprehensively and reason, and output the tool invocation in JSON format, with the JSON content enclosed in [].

# INSTRUCTION: Construct a railway with a width of 30 meters and calculate the area of farmland with slopes less than 15 degrees in the vicinity. The railway data is 'railway.shp,' the farmland data is 'farmland.shp,' and the terrain data is 'terrain.tif.'
from gischain.gischain import init_gischain

import os
import llm.gpt4 as gpt4
myllm = gpt4.GPT4()
myllm.set_api_key(os.environ.get("gpt_key"))

# import llm.gpt3_5 as gpt3_5
# gpt_key = 'sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm'
# myllm = gpt3_5.GPT3_5()
# myllm.set_api_key(os.environ.get("gpt_key"))

# import llm.text2sql as text2sql
# text2sql_key = "=="
# myllm = text2sql.Text2SQL()
# myllm.set_api_key(os.environ.get("text2sql_key")))

# import llm.qwen as qwen
# myllm = qwen.QWen()
# myllm.set_api_key(os.environ.get("qwen_key"))

tools = myllm.invoke(text3)
toolstr = [f'工具: {item}' for item in tools]
print('\n'.join(toolstr))
