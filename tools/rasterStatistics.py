desc = """{
    "name":"rasterStatistics",
    "description":"根据矢量面要素内的有效栅格值计算统计量，包括像元个数、像元面积和等，统计值输出到矢量面要素属性表中",
    "inputs":{
        "tiffile":"要被统计的栅格tiff文件",
        "shpfile":"用来进行统计的矢量面要素文件",
        "mode":"统计模式，包括count（像元个数）、area（像元面积和）等",
        "outfield":"统计结果输出到矢量面要素文件中的字段名，长度不能超过10个字符"
    },
    "output":"输出的带统计结果的矢量面要素文件"
}
"""

example = """
指令：求各区县坡度小于10度的面积。区县数据是county.shp，地形数据为terrain.tif。
json:[
{
	"name":"slope",
	"inputs":{
		"tiffile":"terrain.tif"
	},
    "output":"slope.tif"
},
{
	"name":"extractByValues",
	"inputs":{
        "tiffile":"slope.tif",
        "min":0,
        "max":10
	},
    "output":"slope_0_10.tif"
},
{
    "name":"rasterStatistics",
    "inputs":{
        "tiffile":"slope_0_10.tif",
        "shpfile":"county.shp",
        "mode":"area",
        "outfield":"slope_area"
    },
    "output":"county_stat.shp"
}
"""

def check(tool):
    ok = True
    errors = ""
    tiffile = tool["inputs"]["tiffile"]
    shpfile = tool["inputs"]["shpfile"]
    if not tiffile.endswith(".tif"):
        ok = False
        errors += f"对于工具{tool['name']}，输入的tiffile参数必须是tif文件，而不能是{tiffile}；"
    if not shpfile.endswith(".shp"):
        ok = False
        errors += f"对于工具{tool['name']}，输入的shpfile参数必须是shp文件，而不能是{shpfile}；"
    mode = tool["inputs"]["mode"]
    if mode != "count" and mode != "area":
        ok = False
        errors += f"对于工具{tool['name']}，mode参数必须是count或area，而不能是{mode}；"
    outfield = tool["inputs"]["outfield"]
    if len(outfield) > 10:
        ok = False
        errors += f"对于工具{tool['name']}，outfield参数的长度不能超过10个字符，{outfield}的长度为{len(outfield)}，超过了10个字符；"
    return ok, errors

from osgeo import gdal, ogr
import numpy as np
from . import base

def rasterStatistics(tiffile: str, shpfile: str, mode: str, outfield: str, output: str):
    # 忽略gdal的warning
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    # 处理编码问题
    encoding = base.read_shp_encoding(shpfile)
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", encoding)

    # Open the raster file and get pixel size
    raster = gdal.Open(tiffile, gdal.GA_ReadOnly)
    band = raster.GetRasterBand(1)
    geotransform = raster.GetGeoTransform()
    pixel_size_x = geotransform[1]
    pixel_size_y = -geotransform[5]  # 考虑到y方向的像素大小为负值
    one_pixel_area = pixel_size_x * pixel_size_y
    
    # Open the shapefile
    shp = ogr.Open(shpfile) 
    layer = shp.GetLayer()

    # Create a new field in the shapefile
    output_driver = ogr.GetDriverByName("ESRI Shapefile")
    output_dataset = output_driver.CreateDataSource(output)
    output_layer = output_dataset.CopyLayer(layer, layer.GetName())
    output_layer.CreateField(ogr.FieldDefn(outfield, ogr.OFTReal))
    # 在 field 中先写入对象的id，用来做后续栅格化的burn_value
    ids = []
    for feature in output_layer:
        id = feature.GetFID() + 1
        ids.append(id)
        feature.SetField(outfield, id)
        output_layer.SetFeature(feature)

    # Create a memory raster to rasterize the shpaefile
    memdrv = gdal.GetDriverByName('MEM')
    memraster = memdrv.Create('', raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_UInt32)
    memraster.SetProjection(raster.GetProjection())
    memraster.SetGeoTransform(raster.GetGeoTransform())
    memraster.GetRasterBand(1).Fill(0)

    # Rasterize the shapefile layer to the memory raster
    options=[f"attribute={outfield}", "ALL_TOUCHED=False"]
    gdal.RasterizeLayer(memraster, [1], output_layer, options=options)
        
    # Read memory raster as array
    rasterArray = np.array(memraster.GetRasterBand(1).ReadAsArray()).flatten()
    memraster = None
    counts = np.bincount(rasterArray[rasterArray != 0])
    results = counts[ids]
    if mode == "count":
        for index, feature in enumerate(output_layer):
            feature.SetField(outfield, results[index])
            output_layer.SetFeature(feature)
    elif mode == "area":
        areas = results * one_pixel_area
        for index, feature in enumerate(output_layer):
            feature.SetField(outfield, areas[index])
            output_layer.SetFeature(feature)
        
    output_dataset.SyncToDisk()
    output_dataset = None
    shp = None
    raster = None
    base.write_shp_encoding(output, encoding) # 写入编码信息
    return output
