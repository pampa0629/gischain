import geopandas as gpd
from . import base

# desc = """{
#     "name":"filter",
#      "description":"根据输入的条件对要素进行属性过滤，只支持矢量数据，不支持栅格数据和地形数据"
# }"""

# desc = """
# {
#     "name":"filter",
#     "description":"根据输入的条件对要素进行属性过滤，只支持矢量数据，不支持栅格数据和地形数据",
#     "inputs":{
#         "datafile":"要过滤的数据文件，仅支持shape文件",
#         "where":"过滤条件，类似于SQL语句中的where子句，例如：land_type=='005'"
#     },
#     "output":"过滤后的结果数据"
# }
# """

name = "filter" 
description="根据输入的条件对要素进行属性过滤，只支持矢量数据，不支持栅格数据和地形数据"
parameters = {
    "datafile": {
        "type": "string",
        "description": "要过滤的数据文件，仅支持shape文件"
    },
    "where": {
        "type": "string",
        "description": "过滤条件，类似于SQL语句中的where子句，例如：land_type=='005'"
    },
    "output":{
        "type": "string",
        "description": "过滤后的结果数据文件"
    }
}

import json
from . import fc
core = fc.build_fc_core(name, description, parameters)
# core_desc = json.dumps(core_obj) # 算子核心内容的字符描述
# 直接给function call的tools参数中用的
fc_obj = fc.build_fc_obj(core)

example = ""

# """
# 指令：从土地数据中提取出耕地的数据，土地类型字段是land_type，耕地类型的值为005；土地数据是land.shp。
# json: [{
# 	"name":"filter",
# 	"inputs":{
# 		"datafile":"land.shp",
# 		"where":"land_type=='005'"
# 	},
#     "output":"farm_land.shp"
# }]
# """

def check(tool):
    datafile = tool["parameters"]["inputs"]["datafile"]
    # 必须是shp文件
    if not datafile.endswith(".shp"):
        return False, f"对于工具{tool['name']}，输入的datafile参数必须是shp文件，而不能是{datafile}；"
    return True, ""

# 处理类似“City IS NOT NULL”的情况
def deal_no_null(where:str):
    # result_df = df.query('column_name.notna()')
    if "IS NOT NULL" in where:
        where = where.replace("IS NOT NULL", ".notna()")
        # 去掉中间的空格
        where = where.replace(" ", "")
    return where


def filter(datafile:str, where:str, output:str):
    gdf = gpd.read_file(datafile)
    print("before:",where)
    where = deal_no_null(where)
    print("after:",where)
    filtered_gdf = gdf.query(where)
    print(f"过滤前共有{len(gdf)}个要素，过滤后共有{len(filtered_gdf)}个要素")
    filtered_gdf.to_file(output, encoding=base.read_shp_encoding(datafile))
    return output

