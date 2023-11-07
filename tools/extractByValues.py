from osgeo import gdal
import numpy as np

desc = """
{
    "name":"extractByValues",
    "description":"根据给定的最小最大值提取栅格数据，对最小最大值范围之外的像元赋值为NoData",
    "inputs":{
        "tiffile":"被提取的栅格tiff文件",
        "min":"最小值",
        "max":"最大值"
    },
    "output":"提取后的栅格tiff文件"
}
"""

example = """
指令：需要获取海拔在200米以下的范围，地形数据是 terrain.tif。
json: [{
	"name":"extractByValues",
	"inputs":{
		"tiffile":"terrain.tif",
        "min":0,
        "max":200
	},
    "output":"terrain_0_200.tif"
}]

指令：需要获取坡度在10-20度之间的范围，坡度数据是 slope.tif。
json: [{
	"name":"extractByValues",
	"inputs":{
		"tiffile":"slope.tif",
        "min":10,
        "max":20
	},
    "output":"slope_10_20.tif"
}]
"""
def check(tool):
    tiffile = tool["inputs"]["tiffile"]
    # 必须是tif文件
    if not tiffile.endswith(".tif"):
        return False, f"对于工具{tool['name']}，输入的tiffile参数必须是tif文件，而不能是{tiffile}；"
    return True, ""

def extractByValues(tiffile:str, min:float, max:float, output:str):
    # 防止部分llm给出的是字符串
    min = float(min) 
    max = float(max) 

    # 打开输入文件
    ds = gdal.Open(tiffile)
    if ds is None:
        print(f"无法打开输入文件{tiffile}")
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
