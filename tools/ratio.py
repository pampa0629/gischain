import geopandas as gpd

desc = """{
	"name":"ratio",
	"description":"计算比率",
	"inputs":{
		"value1":"分子的json文件",
        "value2":"分母的json文件"
	},
    "output":"分子除以分母得到的比例结果，存储到json中"
}"""

example = """
指令：计算两个数值相除的比例。
json: [{
	"name":"ratio",
	"inputs":{
		"value1":"value1.json",
        "value2":"value2.json"
	},
    "output":"ratio.json"
}]"""

def read_json_value(datafile):
    import json
    # 打开并读取 JSON 文件
    with open(datafile, "r") as file:
        value = json.load(file)
    value = float(value)
    return value


def ratio(value1:str, value2:str,output=None):
    value1 = read_json_value(value1)
    value2 = read_json_value(value2)
    result = value1 / value2

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
    

