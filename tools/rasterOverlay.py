import numpy as np
from osgeo import gdal

disc = """
{
	name:rasterOverlay,
	description:两个栅格tiff文件做叠加分析,结果文件若datafile2对应像元有值，则为datafile1中的原值，若datafile2中对应像元值为nodata，则结果中对应像元值为nodata,
	inputs:{
		datafile1:参与叠加分析的tiff文件1,
		datafile2:参与叠加分析的tiff文件2
	},
    output:叠加分析结果文件，仍然为tiff文件
}
"""

def rasterOverlay(datafile1:str, datafile2:str, output:str):
    # 打开第一个栅格数据集
    datafile1 = gdal.Open(datafile1)
    if datafile1 is None:
        print("无法打开 datafile1.tif")
        exit(1)

    # 打开第二个栅格数据集
    datafile2 = gdal.Open(datafile2)
    if datafile2 is None:
        print("无法打开 datafile2.tif")
        exit(1)

    # 获取第一个数据集的波段
    band1 = datafile1.GetRasterBand(1)

    # 获取第二个数据集的波段
    band2 = datafile2.GetRasterBand(1)

    # 读取数据集1和数据集2的像元值
    data1 = band1.ReadAsArray()
    data2 = band2.ReadAsArray()

    # 获取NoData值
    nodata_value1 = band1.GetNoDataValue()
    nodata_value2 = band2.GetNoDataValue()

    # 根据规则生成结果数组
    result = np.where(data2 != nodata_value2, data1, nodata_value1)

    # 创建输出栅格数据集
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output, datafile1.RasterXSize, datafile1.RasterYSize, 1, band1.DataType)

    # 写入结果数组到输出数据集
    output_band = output_ds.GetRasterBand(1)
    output_band.WriteArray(result)
    # 设置nodata值
    output_band.SetNoDataValue(band1.GetNoDataValue())

    # 设置地理参考信息
    output_ds.SetProjection(datafile1.GetProjection())
    output_ds.SetGeoTransform(datafile1.GetGeoTransform())

    # 关闭数据集
    datafile1 = None
    datafile2 = None
    output_ds = None
    return output


def rasterOverlay2(datafile1:str, datafile2:str, output:str):
    # 打开第一个栅格数据集
    ds1 = gdal.Open(datafile1)
    band1 = ds1.GetRasterBand(1)
    data1 = band1.ReadAsArray()

    # 打开第二个栅格数据集
    ds2 = gdal.Open(datafile2)
    band2 = ds2.GetRasterBand(1)
    data2 = band2.ReadAsArray()

    # 执行overlay操作
    overlay_result = np.logical_and(data1 != band1.GetNoDataValue(), data2 != band2.GetNoDataValue()).astype(np.uint8)

    # 创建输出栅格数据集
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(output, ds1.RasterXSize, ds1.RasterYSize, 1, gdal.GDT_Byte)
    out_band = out_ds.GetRasterBand(1)

    # 写入overlay结果到输出栅格数据集
    out_band.WriteArray(overlay_result)

    # 设置NoData值
    out_band.SetNoDataValue(band1.GetNoDataValue())

    # 设置地理参考信息
    out_ds.SetProjection(ds1.GetProjection())
    out_ds.SetGeoTransform(ds1.GetGeoTransform())

    # 关闭数据集
    ds1 = None
    ds2 = None
    out_ds = None
    return output
