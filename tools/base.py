# 

def isVectorFile(filename):
    return filename.endswith('.shp')  # or filename.endswith('.geojson') or filename.endswith('.json')

def isRasterFile(filename):
    return filename.endswith('.tif')  # or filename.endswith('.jpg') or filename.endswith('.png')