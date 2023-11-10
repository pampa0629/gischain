desc = """{
    "name":"groupStatistics",
    "description":"分组统计功能，根据分组字段对每个组内的数据进行统计；等同于sql的：select sum(infield) as outfield from datafile group by groupby",
    "inputs":{
        "datafile":"要进行分组统计的数据文件，支持shape、csv、json等格式",
        "infield":"要统计数据的字段名，当前只支持一个字段，不支持多个字段同时统计",
        "mode":"统计模式，包括count（个数）、sum（求和）等",
        "groupby":"进行分组统计的字段名",
        "outfield":"输出的结果的字段名"
    },
    "output":"输出的带统计结果的文件，支持csv、json等格式"
}
"""

example = """
指令：统计一个地区内所有县的耕地面积的总和；耕地数据是 farmland.shp，地区字段是"City"，县字段是"Name"，面积字段是“Area”。
json: [{
	"name":"groupStatistics",
	"inputs":{
		"datafile":"farmland.shp",
		"infield":"Area",
        "mode":"sum",
        "groupby":"City",
        "outfield":"Area_sum_by_City"
    },
    "output":"farmland_area_sum.shp"
}]
"""

def check(tool):
    datafile = tool["inputs"]["datafile"]
    # 必须是shape、csv、json等格式
    if not datafile.endswith(".shp") and not datafile.endswith(".csv") and not datafile.endswith(".json"):
        return False, f"对于工具{tool['name']}，输入的datafile参数必须是shp、csv或json文件，而不能是{datafile}；"
    # 输入字段必须是一个字段
    # 增加输出
    return True, ""

from . import base
import pandas as pd

def groupStatistics(datafile, infield, mode, groupby, outfield, output):
    df = base.read_dataframe(datafile)

    # 根据分组字段进行统计
    if mode == 'count':
        result = df.groupby(groupby).size().reset_index(name=outfield)
    elif mode == 'sum':
        result = df.groupby(groupby)[infield].sum().reset_index(name=outfield)
    # 可以根据需要添加其他统计模式的支持
    # print(result)

    # if output.endswith(".shp"):
    #     encoding=base.read_shp_encoding(datafile)        
    base.write_dataframe(result, output)
    return output