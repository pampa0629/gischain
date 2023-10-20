from osgeo import gdal
import numpy as np

disc = """
{
    name:extractByValues,
    description:根据最大最小值提取栅格数据，对最大最小值范围之外的像元赋值为NoData,
    inputs:{
        tifffile:被提取的栅格tiff文件,
        min:最小值,
        max:最大值
    },
    output:提取后的栅格tiff文件
}
"""

def extractByValues(tifffile:str, min:float, max:float, output:str):
    # 防止部分llm给出的是字符串
    min = float(min) 
    max = float(max) 

    # 打开输入文件
    ds = gdal.Open(tifffile)
    if ds is None:
        print("无法打开输入文件{tifffile}")
        exit(1)

    # 读取栅格数据
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()

    # 将超出范围的值设置为无数据值
    data[data < min] = band.GetNoDataValue()
    data[data > max] = band.GetNoDataValue()

    # 创建输出文件
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(output, ds.RasterXSize, ds.RasterYSize, 1, band.DataType)

    if out_ds is None:
        print("无法创建输出文件")
        exit(1)

    out_band = out_ds.GetRasterBand(1)

    # 写入处理后的数据
    out_band.WriteArray(data)

    # 设置无数据值
    out_band.SetNoDataValue(band.GetNoDataValue())

    # 将地理参考信息和投影信息从输入文件复制到输出文件
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.SetProjection(ds.GetProjection())

    # 关闭数据集
    ds = None
    out_ds = None
    return output
