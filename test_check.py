import os
# 这里修改为 config.ini 并把该ini文件中的key值改为自己的key
os.environ["config_file"] = "myconfig.ini"

result = """
[\n    {\n        \"name\": \"slope\",\n        \"inputs\": {\n            \"tiffile\": \"data/terrain.tif\"\n        },\n        \"output\": \"data/temp/slope.tif\"\n    },\n    {\n        \"name\": \"extractByValues\",\n        \"inputs\": {\n            \"tiffile\": \"data/temp/slope.tif\",\n            \"min\": 0,\n            \"max\": 10\n        },\n        \"output\": \"data/temp/slope_0_10.tif\"\n    },\n    {\n        \"name\": \"overlay\",\n        \"inputs\": {\n            \"datafile1\": \"data/temp/slope_0_10.tif\",\n            \"datafile2\": \"data/temp/terrain_0_100.tif\"\n        },\n  
      \"output\": \"data/temp/overlay_slope_terrain_0_100.tif\"\n    },\n    {\n        \"name\": \"overlay\",\n        \"inputs\": {\n            \"datafile1\": \"data/temp/overlay_slope_terrain_0_100.tif\",\n            \"datafile2\": \"data/farmland.shp\"\n        },\n        \"output\": \"data/temp/overlay_slope_farmland_0_100.tif\"\n    },\n    {\n        \"name\": \"area\",\n        \"inputs\": {\n            \"datafile\": \"data/temp/overlay_slope_farmland_0_100.tif\"\n        },\n        \"output\": \"data/output/area_result.json\"\n    }\n]
"""

import json
tools = json.loads(result)
# print(tools)

print(f"解析得到的工具有{len(tools)}个，列表和参数如下:")
toolstr = [f'工具: {item}' for item in tools]
print('\n'.join(toolstr))

# from gischain.check import check_tools
from gischain import check
instruction = "修一条铁路，宽度为50米，需要计算占用周边坡度小于10度、海拔小于100米的耕地面积。铁路数据是railway.shp，耕地数据是farmland.shp，地形数据是terrain.tif。"
ok, errors = check.check_tools(tools, instruction)
print(f"检查结果：{ok}, {errors}")