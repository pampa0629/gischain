import geopandas as gpd

desc = """
{
        "name":"filter",
        "description":"根据条件对要素进行过滤",
        "inputs":{
                "datafile":"要过滤的数据文件",
                "where":"过滤条件"
        },
    "output":"过滤后的结果数据"
}
"""

example = """
指令：从土地数据中提取出耕地的数据，土地类型字段是land_type，耕地类型的值为005；土地数据是land.shp。
json: [{
	"name":"filter",
	"inputs":{
		"datafile":"land.shp",
		"where":"land_type=='005'"
	},
    "output":"farm_land.shp"
}]
"""
import os

def check(tool):
    datafile = tool["inputs"]["datafile"]
    # 必须是shp文件
    if not datafile.endswith(".shp"):
        return False, f"对于工具{tool['name']}，输入的datafile参数必须是shp文件，而不能是{datafile}；"
    return True, ""

def read_encoding(shapefile):
    cpgfile_path = shapefile.replace('.shp', '.cpg')
    if os.path.exists(cpgfile_path):
        with open(cpgfile_path, 'r') as cpgfile:
            encoding = cpgfile.read().strip()
            return encoding
    return 'utf-8'

def filter(datafile:str, where:str, output:str):
    gdf = gpd.read_file(datafile)
    filtered_gdf = gdf.query(where)
    filtered_gdf.to_file(output, encoding=read_encoding(datafile))
    return output

