from osgeo import gdal
from osgeo import gdalconst

disc = """
{
    name:slope,
    description:根据地形数据计算坡度,
    inputs:{
        tifffile:栅格地形tiff文件
    },
    output:坡度计算结果的栅格tiff文件
}
"""

def slope(tifffile:str, output:str):
    # 打开DEM文件
    dem = gdal.Open(tifffile, gdalconst.GA_ReadOnly)
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