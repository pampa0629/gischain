import geopandas as gpd

desc = """{
	"name":"dissolve",
	"description":"数据融合",
	"inputs":{
		"datafile":"需要进行融合的数据文件"
	},
    "output":"融合后的数据文件"
}"""

example = """
指令：把所有空间对象融合为一个对象。数据文件是region.shp。
json: [{
	"name":"dissolve",
	"inputs":{
		"datafile":"region.shp"
	},
    "output":"region_dissolve.shp"
}]"""

def dissolve(datafile:str, output:str):
    data = gpd.read_file(datafile)
    result = data.dissolve(by=None)
    result.to_file(output)
    return output

from . import base
def check(tool):
    datafile = tool["inputs"]["datafile"]
    # 得到数据文件的后缀名
    if datafile.endswith('.shp') == False:
       return False, f"{datafile} 现在只支持shp文件；"
    return True, ""
    

