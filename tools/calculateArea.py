
def calculateArea(datafile:str, output) -> float:
    # print("calculateArea:",datafile)
    import geopandas as gpd
    data = gpd.read_file(datafile)
    result = sum(data.area)
    output = result
    return result

disc = """
{
	name:calculateArea,
	discription:计算面积，并求和,
	inputs:{
		datafile:要求面积的数据文件
	},
    output:面积结果
}
"""
