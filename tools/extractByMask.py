from osgeo import gdal, ogr
import numpy as np

disc = """
{
        name:extractByMask,
        description:根据面数据对栅格数据做掩膜，对掩膜之外的像元赋值为NoData,
        inputs:{
                tifffile:被提取的栅格tiff文件,
                maskfile:掩膜层，shp面数据文件
        },
    output:掩膜提取后的栅格tiff文件
}
"""

def extractByMask(tifffile:str, maskfile:str, output:str):
    # 打开栅格数据集
    input_raster = gdal.Open(tifffile)
    if input_raster is None:
        print("无法打开输入栅格数据集")
        exit(1)
    input_band = input_raster.GetRasterBand(1)
    nodata = input_band.GetNoDataValue()

    # 打开矢量多边形文件
    vector_file = ogr.Open(maskfile)
    if vector_file is None:
        print("无法打开矢量多边形文件")
        exit(1)
    vector_layer = vector_file.GetLayer()

    # 创建掩膜
    mask_ds = gdal.GetDriverByName('MEM').Create('', input_raster.RasterXSize, input_raster.RasterYSize, 1, input_band.DataType)

    # 设置坐标范围、nodata值和仿射变换信息
    mask_ds.SetProjection(input_raster.GetProjection())
    mask_ds.SetGeoTransform(input_raster.GetGeoTransform())
    mask_band = mask_ds.GetRasterBand(1)
    mask_band.SetNoDataValue(nodata)

    # 根据面数据生成掩膜
    data = mask_band.ReadAsArray()
    # 先设置为无数据值
    data[:] = nodata
    mask_band.WriteArray(data)
    gdal.RasterizeLayer(mask_ds, [1], vector_layer, burn_values=[1])

    # 根据输入tiff和掩膜数据，生成结果数据
    input_array = input_raster.ReadAsArray()
    output_array = np.where(mask_ds.ReadAsArray() != nodata, input_array, nodata)

    # 创建输出栅格数据集
    output_ds = gdal.GetDriverByName('GTiff').Create(output, input_raster.RasterXSize, input_raster.RasterYSize, 1, input_band.DataType)
    output_band = output_ds.GetRasterBand(1)
    output_band.WriteArray(output_array)
    output_band.SetNoDataValue(nodata)

    # 设置地理参考信息
    output_ds.SetProjection(input_raster.GetProjection())
    output_ds.SetGeoTransform(input_raster.GetGeoTransform())

    # 关闭数据集
    input_raster = None
    vector_file = None
    mask_ds = None
    output_ds = None

    return output

