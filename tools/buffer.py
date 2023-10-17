import geopandas as gpd

disc = """
{
	name:buffer,
	description:得到缓冲区,
	inputs:{
		datafile:要求缓冲区的数据文件
		radius:缓冲区半径
	},
    output:缓冲区结果文件
}
"""

def buffer(datafile:str, radius:float, output:str):
    data = gpd.read_file(datafile)
    radius = float(radius) # 防止部分llm给出的是字符串
    result = data.buffer(radius)
    result.to_file(output)
    return output


