import geopandas as gpd
import os
from osgeo import gdal
import numpy as np

disc = """
{
	name:calculateArea,
	description:计算面积；如果输入是矢量面文件，则求所有面的面积和；如果输入是栅格文件，则求所有非nodata像元的面积和
	inputs:{
		datafile:要求面积的数据文件
    },
    output:面积结果
}
"""

def calculateArea(datafile:str, output=None) -> float:
    _, ext = os.path.splitext(datafile)
    if ext == ".tif" or ext == ".tiff":
        result = calculateAreaFromRaster(datafile)
    elif ext == ".shp":
        result = calculateAreaFromVector(datafile)
    if output != None:
        with open(output, "w") as f:
            f.write(str(result))
    return result

def calculateAreaFromRaster(datafile:str) -> float:
    # 打开TIFF文件
    tiff_dataset = gdal.Open(datafile)
    # 获取TIFF文件的波段和NoData值
    band = tiff_dataset.GetRasterBand(1)
    no_data = band.GetNoDataValue()

    # 读取TIFF数据为NumPy数组
    tiff_array = band.ReadAsArray()
    # 计算非NoData像元的面积
    non_nodata_pixels = np.count_nonzero(tiff_array != no_data)

    # 获取像元大小和地理参考信息
    pixel_area = abs(tiff_dataset.GetGeoTransform()[1] * tiff_dataset.GetGeoTransform()[5])
    total_area = non_nodata_pixels * pixel_area

    return total_area

def calculateAreaFromVector(datafile:str) -> float:
    data = gpd.read_file(datafile)
    result = sum(data.area)
    output = result
    return result
