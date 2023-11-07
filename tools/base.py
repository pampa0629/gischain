# 

def isVectorFile(filename):
    return filename.endswith('.shp')  # or filename.endswith('.geojson') or filename.endswith('.json')

def isRasterFile(filename):
    return filename.endswith('.tif')  # or filename.endswith('.jpg') or filename.endswith('.png')

# 文件必须存在
def check_file_exists(datafile):
    import os    
    if os.path.exists(datafile) == False:
        return False, f"{datafile} 文件不存在，请核实文件的来源，或者是否组合出正确的文件路径；"
    return True, ""