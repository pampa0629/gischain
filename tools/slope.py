from osgeo import gdal
from osgeo import gdalconst

desc = """
{
    "name":"slope",
    "description":"根据地形数据计算坡度",
    "inputs":{
        "tiffile":"栅格地形tiff文件"
    },
    "output":"坡度计算结果的栅格tiff文件"
}
"""

example = """
指令：需要获取坡度数据，地形数据是 terrain.tif。
json: [{
	"name":"slope",
	"inputs":{
		"tiffile":"terrain.tif"
	},
    "output":"slope.tif"
}]
"""
def check(tool):    
    inputs = tool["inputs"]
    for key in inputs:
        if key != "tiffile":
            return False, f"对于工具{tool['name']}，输入的参数必须是tiffile，而不能是{key}；"
    return True, ""

def slope(tiffile:str, output:str):
    # 打开DEM文件
    dem = gdal.Open(tiffile, gdalconst.GA_ReadOnly)
    if dem is None:
        print("Failed to open the DEM file.")
        return None

    # 生成坡度文件
    gdal.DEMProcessing(output, dem, processing='slope', 
                       scale=1.0, alg='Horn',band=1,format='GTiff',
                       slopeFormat="degree", zeroForFlat=1, computeEdges=False)

    # 关闭数据集
    dem = None
    return output