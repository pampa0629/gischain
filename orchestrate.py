text = """
[
    {
        "name": "buffer",
        "inputs": {
            "datafile": "data/railway.shp",
            "radius": 500
        },
        "output": "data/railway_buffer.shp"
    },
    {
        "name": "overlay",
        "inputs": {
            "datafile1": "data/railway_buffer.shp",
            "datafile2": "data/land.shp"
        },
        "output": "data/buffer_land.shp"
    },
    {
        "name": "slope",
        "inputs": {
            "tifffile": "data/terrain.tif"
        },
        "output": "data/slope.tif"
    },
    {
        "name": "extractByValues",
        "inputs": {
            "tifffile": "data/slope.tif",
            "min": 0,
            "max": 10
        },
        "output": "data/slope_10.tif"
    },
    {
        "name": "polygon2mask",
        "inputs": {
            "shpfile": "data/buffer_land.shp",
            "tiffile": "data/terrain.tif"
        },
        "output": "data/buffer_land_mask.tif"
    },
    {
        "name": "rasterOverlay",
        "inputs": {
            "datafile1": "data/slope_10.tif",
            "datafile2": "data/buffer_land_mask.tif"
        },
        "output": "data/slope_land.tif"
    },
    {
        "name": "calculateArea",
        "inputs": {
            "datafile": "data/slope_land.tif"
        },
        "output": "data/area_result"
    }
]
"""
import json
tool_list = json.loads(text)

from tools import define
result = ""
for tool in tool_list:
    # python只支持一个可变参数，这句话把output参数加上
    tool['inputs']['output'] = tool['output'] 
    result = define.call_tool(tool['name'], **tool['inputs'])
    print(f"工具 {tool['name']} 的执行结果为：{result}")
print(result)