import geopandas as gpd
from . import base

desc = """
{
    "name":"filter",
    "description":"根据输入的条件对要素进行属性过滤，只支持矢量数据，不支持栅格数据和地形数据",
    "inputs":{
        "datafile":"要过滤的数据文件，仅支持shape文件",
        "where":"过滤条件，类似于SQL语句中的where子句，例如：land_type=='005'"
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

def check(tool):
    datafile = tool["inputs"]["datafile"]
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

