
text = """
[
    {
        "name": "buffer",
        "inputs": {
            "datafile": "data/railway.shp",
            "radius": "50"
        },
        "output": "data/temp/railway_buffer.shp"
    },
    {
        "name": "filter",
        "inputs": {
            "datafile": "data/land.shp",
            "where": "City=='常德市'"
        },
        "output": "data/temp/farm_land.shp"
    },
    {
        "name": "slope",
        "inputs": {
            "tiffile": "data/terrain.tif"
        },
        "output": "data/temp/slope.tif"
    },
    {
        "name": "extractByValues",
        "inputs": {
            "tiffile": "data/temp/slope.tif",
            "min": "0",
            "max": "10"
        },
        "output": "data/temp/slope_less_10.tif"
    },
    {
        "name": "extractByValues",
        "inputs": {
            "tiffile": "data/terrain.tif",
            "min": "0",
            "max": "100"
        },
        "output": "data/temp/altitude_less_100.tif"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/railway_buffer.shp",
            "datafile2": "data/temp/farm_land.shp"
        },
        "output": "data/temp/farm_land_in_buffer.shp"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/farm_land_in_buffer.shp",
            "datafile2": "data/temp/slope_less_10.tif"
        },
        "output": "data/temp/farm_land_on_slope.tif"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/temp/farm_land_on_slope.tif",
            "datafile2": "data/temp/altitude_less_100.tif"
        },
        "output": "data/temp/farm_land_on_slope_altitude.tif"
    },
    {
        "name": "area",
        "inputs": {
            "datafile": "data/temp/farm_land_on_slope_altitude.tif"
        },
        "output": "data/output/final_area.json"
    }
]
"""

import os
# 这里修改为 config.ini 并把该ini文件中的key值改为自己的key
os.environ["config_file"] = "myconfig.ini"

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
