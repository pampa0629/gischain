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

import os
# 读取shp文件的编码
def read_shp_encoding(shapefile):
    cpgfile_path = shapefile.replace('.shp', '.cpg')
    if os.path.exists(cpgfile_path):
        with open(cpgfile_path, 'r') as cpgfile:
            encoding = cpgfile.read().strip()
            return encoding
    return 'utf-8'

# 生成shp文件配套的cpg文件
def write_shp_encoding(shapefile, encoding):
    cpgfile_path = shapefile.replace('.shp', '.cpg')
    with open(cpgfile_path, 'w') as cpgfile:
        cpgfile.write(encoding)


import pandas as pd
import geopandas as gpd

# 读取文件，转换为dataframe
def read_dataframe(datafile):
    if datafile.endswith(".csv"):
        df = pd.read_csv(datafile)
    elif datafile.endswith(".json"):
        df = pd.read_json(datafile)
    elif datafile.endswith(".shp"):
        df = gpd.read_file(datafile)
    else:
        raise Exception(f"不支持的文件类型：{datafile}")
    return df

from . import base
def write_dataframe(df, output):
    if output.endswith(".csv"):
        df.to_csv(output, index=False)
    elif output.endswith(".json"):
        df.to_json(output, orient="records")
    # elif output.endswith(".shp"):
    #     df.to_file(output, encoding=encoding)
    else:
        raise Exception(f"不支持的文件类型：{output}")