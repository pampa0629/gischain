from osgeo import gdal, ogr, osr

disc = """
{
	name:contourPolygon,
	description:从栅格tiff文件中提取等值面,
	inputs:{
		datafile:要提取的栅格tiff文件,
		value:等值面的值
	},
    output:等值面结果shp文件
}
"""

# 当前的实现有问题，不能很好的解决从等值线到等值面的封闭问题
def contourPolygon(datafile:str, value:float, output:str):
    pass # todo
    return output 

    # 打开TIFF文件
    raster = gdal.Open(datafile)
    if raster is None:
        raise Exception("无法打开TIFF文件")

    # 获取栅格数据
    band = raster.GetRasterBand(1)
    srs = raster.GetSpatialRef()
    
    # 创建shp文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    import time
    current_time = time.perf_counter() # 获取微妙级别的时间，构造临时文件
    temp_dir = "./data/temp{current_time}.shp".format(current_time=current_time)
    tempLine = driver.CreateDataSource(temp_dir) 
    templayer = tempLine.CreateLayer("", srs, ogr.wkbLineString) ## 

    # 生成等值线
    gdal.ContourGenerate(band, 0, 0, [0,value],0,0, templayer, -1, -1)
    # 及时关闭，便于后续线转面时打开使用
    templayer = None
    tempLine = None

    # 线转面
    line2polygon(temp_dir,output)

    # 删除临时的线shp文件
    # driver.DeleteDataSource(temp_dir)

    # 关闭tiff数据
    raster = None
    return output

def line2polygon(line_shp,polygon_shp):
    import geopandas as gpd
    from shapely.geometry import Polygon

    # 读取线形状文件
    gdf_line = gpd.read_file(line_shp)
    # 提取所有线的几何对象
    geometries = gdf_line.geometry
    # 将线的两头连接起来，并创建多边形
    polygons = [Polygon(geom.coords) for geom in geometries]
    # 创建一个新的Geopandas GeoDataFrame
    gdf_polygon = gpd.GeoDataFrame(geometry=polygons)
    # 保存多边形形状文件
    gdf_polygon.to_file(polygon_shp)