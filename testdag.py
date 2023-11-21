
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

if __name__ == "__main__":
    tools = json.loads(text)
    result = rundag(tools, show=True, multirun=False)
    # base.print_everything(result)
    # from pprint import pprint
    # pprint(result)
    # print_cvs(result)
