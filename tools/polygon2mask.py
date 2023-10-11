from osgeo import gdal, ogr
import numpy as np

disc = """
{
	name:polygon2mask,
	description:把polygon转换为mask，在polygon之内的像元值为1，之外的像元值为no data; 要生成的栅格文件的分辨率、坐标系等信息，拷贝输入的tiff文件的信息,
	inputs:{
		shpfile:要进行栅格转换的矢量多边形文件,
		tiffile:作为模板的栅格文件
	},
    output:生成的mask栅格文件
}
"""

def polygon2mask(shpfile:str, tiffile:str, output:str):
    # 打开矢量多边形文件
    vector_file = ogr.Open(shpfile)
    if vector_file is None:
        print("无法打开矢量多边形文件")
        exit(1)

    # 获取矢量图层
    vector_layer = vector_file.GetLayer()

    # 打开栅格数据集
    input_raster = gdal.Open(tiffile)
    if input_raster is None:
        print("无法打开输入栅格数据集")
        exit(1)
    projection = input_raster.GetProjection()
    geotransform = input_raster.GetGeoTransform()
    input_band = input_raster.GetRasterBand(1)
    nodata = input_band.GetNoDataValue()

    # 创建输出栅格数据集
    driver = gdal.GetDriverByName('GTiff') # GTiff
    output_tiff = driver.Create(output, input_raster.RasterXSize, input_raster.RasterYSize, 1, input_band.DataType)

    # 设置坐标范围、nodata值和仿射变换信息
    output_tiff.SetProjection(projection)
    output_tiff.SetGeoTransform(geotransform)
    output_band = output_tiff.GetRasterBand(1)
    output_band.SetNoDataValue(nodata)

    data = output_band.ReadAsArray()
    # 先都设置为无数据值
    data[:] = nodata
    output_band.WriteArray(data)

    gdal.RasterizeLayer(output_tiff, [1], vector_layer, burn_values=[1])
    
    # 关闭数据集
    vector_file = None
    input_raster = None
    output_tiff = None
    return output