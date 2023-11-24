
text = """
[{"name": "buffer", "inputs": {"datafile": "data/railway.shp", "radius": 25}, "output": "data/temp/railway_buffer.shp"}, {"name": "slope", "inputs": {"tiffile": "data/terrain.tif"}, "output": "data/temp/slope.tif"}, {"name": "extractByValues", "inputs": {"tiffile": "data/temp/slope.tif", "min": 0, "max": 10}, "output": "data/temp/slope_0_10.tif"}, {"name": "extractByValues", "inputs": {"tiffile": "data/terrain.tif", "min": 0, "max": 100}, "output": "data/temp/terrain_0_100.tif"}, {"name": "overlay", "inputs": {"datafile1": "data/temp/railway_buffer.shp", "datafile2": "data/temp/slope_0_10.tif"}, "output": "data/temp/overlay_railway_slope.tif"}, {"name": "overlay", "inputs": {"datafile1": "data/temp/overlay_railway_slope.tif", "datafile2": "data/temp/terrain_0_100.tif"}, "output": "data/temp/overlay_railway_slope_terrain.tif"}, {"name": "rasterStatistics", "inputs": {"tiffile": "data/temp/overlay_railway_slope_terrain.tif", "shpfile": "data/farmland.shp", "mode": "area", "outfield": "area"}, "output": "data/temp/farmland_area.shp"}, {"name": "groupStatistics", "inputs": {"datafile": "data/temp/farmland_area.shp", "infield": "area", "mode": "sum", "groupby": "City", "outfield": "area_sum"}, "output": "data/output/farmland_area_sum.csv"}, {"name": "sort", "inputs": {"datafile": "data/output/farmland_area_sum.csv", "field": "area_sum", "mode": "desc"}, "output": "data/output/farmland_area_sum_sorted.csv"}]
"""

import json
from  gischain.gischain import rundag
from gischain import base
from gischain import showdag

import os
# 设置禁用文件验证的环境变量
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

def print_cvs(result):
    import pandas as pd
    df = pd.read_csv(result)
    print(df)

import os
import shutil

def delete_files_except(directory, keep_file):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != keep_file:
                file_path = os.path.join(root, file)
                os.remove(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)


if __name__ == "__main__":
    tools = json.loads(text)

    # 指定目录路径和要保留的文件名
    delete_files_except("./data/temp", "_README.md")
    delete_files_except("./data/output", "_README.md")

    result = rundag(tools, show=True, multirun=True)
    # base.print_everything(result)
    # from pprint import pprint
    # pprint(result)
    # print_cvs(result)
