import geopandas as gpd
from osgeo import gdal, ogr
import numpy as np
from . import base

# 启用异常处理
gdal.UseExceptions()

# desc = """{
# 	"name":"overlay",
# 	"description":"叠加分析;支持矢量与矢量、矢量与栅格、栅格与栅格的叠加分析;如果两个输入文件都是矢量，则结果为矢量文件；如果两个输入文件一个为栅格、另一个为矢量，则结果为栅格文件（tif格式）；如果两个输入文件都是栅格，则结果也为栅格文件；目前仅支持intersection模式",
# 	"inputs":{
# 		"datafile1":"参与叠加分析的数据文件1",
# 		"datafile2":"参与叠加分析的数据文件2"
# 	},
#     "output":"叠加分析结果文件"
# }"""


name = "overlay" 
description="叠加分析;支持矢量与矢量、矢量与栅格、栅格与栅格的叠加分析;如果两个输入文件都是矢量，则结果为矢量文件；如果两个输入文件一个为栅格、另一个为矢量，则结果为栅格文件（tif格式）；如果两个输入文件都是栅格，则结果也为栅格文件；目前仅支持intersection模式"
parameters = {
    "datafile1": {
        "type": "string",
        "description": "参与叠加分析的数据文件1"
    },
    "datafile2": {
        "type": "string",
        "description": "参与叠加分析的数据文件2"
    },
    "output":{
        "type": "string",
        "description": "叠加分析结果文件"
    }
}


import json
from . import fc
core = fc.build_fc_core(name, description, parameters)
# core_desc = json.dumps(core_obj) # 算子核心内容的字符描述
# 直接给function call的tools参数中用的
fc_obj = fc.build_fc_obj(core)

example = ""

# example = """
# 指令：求海拔100米以下的耕地面积。耕地数据是farmland.shp，海拔100米以下地形数据为terrain_100.tif。
# json:[{
# 	"name":"overlay",
# 	"inputs":{
# 		"datafile1":"farmland.shp",
# 		"datafile2":"terrain_100.tif"
# 	},
#     "output":"overlay_farmland_terrain_100.tif"
# }]

# 指令：求坡度小于10度之间，海拔小于500米的数据。海拔小于500米的地形数据为terrain_500.tif，坡度小于10度的坡度数据为slope_10.tif。
# json:[
# {
# 	"name":"overlay",
# 	"inputs":{
# 		"datafile1":"slope_20.tif",
# 		"datafile2":"terrain_500.tif"
# 	},
#     "output":"overlay_slope_terrain.tif"
# }]
# """

def check(tool):
    datafile1 = tool["parameters"]["inputs"]["datafile1"]
    datafile2 = tool["parameters"]["inputs"]["datafile2"]
    # 当两个输入文件有一个是tif时，输出必须是tif文件
    if datafile1.endswith('.tif') or datafile2.endswith('.tif'):
        if tool["output"].endswith('.tif') == False:
            return False, f"对于工具{tool['name']}，当两个输入文件有一个是tif时，输出必须是tif文件；"
    return True, ""

def overlay(datafile1:str, datafile2:str, output:str):
    if base.isVectorFile(datafile1) and base.isVectorFile(datafile2):
        return vectorOverlay(datafile1, datafile2, output)
    elif base.isRasterFile(datafile1) and base.isRasterFile(datafile2):
        return rasterOverlay(datafile1, datafile2, output)
    elif (base.isVectorFile(datafile1) and base.isRasterFile(datafile2)) or (base.isVectorFile(datafile2) and base.isRasterFile(datafile1)):
        shpfile = datafile1 if base.isVectorFile(datafile1) else datafile2
        tiffile = datafile1 if base.isRasterFile(datafile1) else datafile2        
        return extractByMask(tiffile, shpfile, output)
    else:
        raise Exception(f"不支持{datafile1}与{datafile2}之间的叠加分析")

def extractByMask(tiffile:str, maskfile:str, output:str):
    # 打开栅格数据集
    input_raster = gdal.Open(tiffile)
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

def vectorOverlay(datafile1:str, datafile2:str, output:str):
    data1 = gpd.read_file(datafile1)
    data2 = gpd.read_file(datafile2)
    result = gpd.overlay(data1, data2, how='intersection')
    result.to_file(output)
    return output

def rasterOverlay(datafile1:str, datafile2:str, output:str):
    # 打开第一个栅格数据集
    datafile1 = gdal.Open(datafile1)
    if datafile1 is None:
        print(f"无法打开 {datafile1}")
        exit(1)

    # 打开第二个栅格数据集
    datafile2 = gdal.Open(datafile2) 
    if datafile2 is None:
        print(f"无法打开 {datafile2}")
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

