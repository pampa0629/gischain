
text = """
[{"name": "buffer", "inputs": {"datafile": "data/railway.shp", "radius": 25}, "output": "data/temp/railway_buffer.shp"}, {"name": "slope", "inputs": {"tiffile": "data/terrain.tif"}, "output": "data/temp/slope.tif"}, {"name": "extractByValues", "inputs": {"tiffile": "data/temp/slope.tif", "min": 0, "max": 10}, "output": "data/temp/slope_0_10.tif"}, {"name": "extractByValues", "inputs": {"tiffile": "data/terrain.tif", "min": 0, "max": 100}, "output": "data/temp/terrain_0_100.tif"}, {"name": "overlay", "inputs": {"datafile1": "data/temp/railway_buffer.shp", "datafile2": "data/temp/slope_0_10.tif"}, "output": "data/temp/overlay_railway_slope.tif"}, {"name": "overlay", "inputs": {"datafile1": "data/temp/overlay_railway_slope.tif", "datafile2": "data/temp/terrain_0_100.tif"}, "output": "data/temp/overlay_railway_slope_terrain.tif"}, {"name": "rasterStatistics", "inputs": {"tiffile": "data/temp/overlay_railway_slope_terrain.tif", "shpfile": "data/farmland.shp", "mode": "area", "outfield": "area"}, "output": "data/temp/farmland_area.shp"}, {"name": "groupStatistics", "inputs": {"datafile": "data/temp/farmland_area.shp", "infield": "area", "mode": "sum", "groupby": "City", "outfield": "area_sum"}, "output": "data/output/farmland_area_sum.csv"}, {"name": "sort", "inputs": {"datafile": "data/output/farmland_area_sum.csv", "field": "area_sum", "mode": "desc"}, "output": "data/output/farmland_area_sum_sorted.csv"}]
"""

import json
# from gischain.showdag import showdag
# from gischain.runtools import multi_run_tools
from  gischain.gischain import rundag
# from ..gischain import run_tools


# import gischain.gischain  as gischain

import os
# 设置禁用文件验证的环境变量
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

if __name__ == "__main__":
    # original_string = "这是一个包含'单引号'的字符串。"
    # text = text.replace("'", "\"")
    tools = json.loads(text)
    # for tool in tools:
    #     # python只支持一个可变参数，这句话把output参数加上
    #     tool['inputs']['output'] = tool['output'] 

    result = rundag(tools, show=True, multirun=False)

    print(result)
