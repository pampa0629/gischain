
def buffer(datafile:str, radius:float, output:str):
    # print("buffer:",datafile,radius)
    import geopandas as gpd
    data = gpd.read_file(datafile)
    result = data.buffer(radius)
    result.to_file(output)
    return output

disc = """
{
	name:buffer,
	discription:得到缓冲区,
	inputs:{
		datafile:要求缓冲区的数据文件
		radius:缓冲区半径
	},
    output:缓冲区结果文件
}
"""



