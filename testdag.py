
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
from gischain.showdag import showdag
from gischain.runtools import multi_run_tools

if __name__ == "__main__":

    tools = json.loads(text)
    # showdag(tools)
    result = multi_run_tools(tools)
    print(result)
