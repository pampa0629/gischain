import geopandas as gpd

disc = """
{
	name:overlay,
	description:叠加分析,
	inputs:{
		datafile1:参与叠加分析的数据文件1,
		datafile2:参与叠加分析的数据文件2
	},
    output:叠加分析结果文件
}
"""

def overlay(datafile1:str, datafile2:str, output:str):
    data1 = gpd.read_file(datafile1)
    data2 = gpd.read_file(datafile2)
    result = gpd.overlay(data1, data2, how='intersection')
    result.to_file(output)
    return output


