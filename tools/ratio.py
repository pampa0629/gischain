import geopandas as gpd

# desc = """{
# 	"name":"ratio",
# 	"description":"计算比率",
# 	"inputs":{
# 		"value1":"分子的json文件",
#         "value2":"分母的json文件"
# 	},
#     "output":"分子除以分母得到的比例结果，存储到json中"
# }"""
# Numerator and Denominator

name = "ratio" 
description="计算比率"
parameters = {
    "numerator": {
        "type": "string",
        "description": "分子的json文件"
    },
    "denominator": {
        "type": "string",
        "description": "分母的json文件"
    },
    "output": {
        "type": "string",
        "description": "分子除以分母得到的比例结果，存储到json中"
    }
}

import json
from . import fc
core = fc.build_fc_core(name, description, parameters)
# core_desc = json.dumps(core_obj) # 算子核心内容的字符描述
# 直接给function call的tools参数中用的
fc_obj = fc.build_fc_obj(core)

example = ""

# example = """
# 指令：计算两个数值相除的比例。
# json: [{
# 	"name":"ratio",
# 	"inputs":{
# 		"value1":"value1.json",
#         "value2":"value2.json"
# 	},
#     "output":"ratio.json"
# }]"""

def read_json_value(datafile):
    import json
    # 打开并读取 JSON 文件
    with open(datafile, "r") as file:
        value = json.load(file)
    value = float(value)
    return value

def ratio(numerator:str, denominator:str,output=None):
    numerator = read_json_value(numerator)
    denominator = read_json_value(denominator)
    result = numerator / denominator

    if output != None:
        with open(output, "w") as f:
            f.write(str(result))
    return output

# from . import base
# def check(tool):
#     datafile = tool["inputs"]["datafile"]
#     # 得到数据文件的后缀名
#     if datafile.endswith('.shp') == False:
#        return False, f"{datafile} 现在只支持shp文件；"
#     return True, ""
    

