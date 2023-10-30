
text = """
[{
    "name": "buffer",
    "inputs": {
        "datafile": "railway.shp",
        "radius": 30
    },
    "output": "railway_buffer.shp"
},
{
    "name": "slope",
    "inputs": {
        "tiffile": "terrain.tif"
    },
    "output": "terrain_slope.tif"
},
{
    "name": "extractByValues",
    "inputs": {
        "tiffile": "terrain_slope.tif",
        "min": 0,
        "max": 15
    },
    "output": "farmland_low_slope.tif"
},

{
    "name": "area",
    "inputs": {
        "datafile": "farmland_low_slope.tif"
    },
    "output": "farmland_low_slope_area.txt"
},

{
    "name": "overlay",
    "inputs": {
        "datafile1": "railway_buffer.shp",
        "datafile2": "farmland_low_slope.tif"
    },
    "output": "railway_buffer_overlay.tif"
},

{
    "name": "area",
    "inputs": {
        "datafile": "railway_buffer_overlay.tif"
    },
    "output": "railway_buffer_overlay_area.txt"
}]

"""

import json
# from gischain.showdag import showdag
# from gischain.runtools import multi_run_tools
import gischain.gischain  as gischain

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

    result = gischain.rundag(tools, show=True, multirun=False)

    print(result)
