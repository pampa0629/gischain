from osgeo import gdal

tifffile = "data/slope.tif"
ds = gdal.Open(tifffile)
if ds is None:
    print("无法打开输入文件{tifffile}")
    exit(1)