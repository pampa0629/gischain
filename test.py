# import tools
from tools.buffer import buffer
from tools.overlay import overlay
from tools.slope import slope
from tools.extractByValues import extractByValues
from tools.extractByMask import extractByMask
from tools.rasterOverlay import rasterOverlay
from tools.polygon2mask import polygon2mask
from tools.calculateArea import calculateArea

# buffer("./data/railway.shp", 5000, "./data/buffer_railway.shp")
# overlay("./data/buffer_railway.shp", "./data/land.shp", "./data/overlay_buffer_land.shp")

# slope("./data/terrain.tif", "./data/slope_terrain.tif")
# extractByValues("./data/slope_terrain.tif", 0, 10, "./data/slope_values.tif")

# extractByValues("./data/terrain.tif", 0, 500, "./data/terrain_values.tif")

# rasterOverlay("./data/slope_values.tif","./data/terrain_values.tif", "./data/overlay_slope_terrain.tif")

# polygon2mask.polygon2mask("./data/overlay_buffer_land.shp", "./data/overlay_slope_terrain.tif", "./data/land_mask.tif")

# extractByMask("./data/overlay_slope_terrain.tif","./data/overlay_buffer_land.shp", "./data/result_land.tif")

print(calculateArea("./data/result_land.tif"))

# text = """
#     [
#         {
#             "name": "buffer",
#             "inputs": {
#                 "datafile": "data/railway.shp",
#                 "radius": 500
#             },
#             "output": "data/railway_buffer.shp"
#         },
#         {
#             "name": "overlay",
#             "inputs": {
#                 "datafile1": "data/railway_buffer.shp",
#                 "datafile2": "data/land.shp"
#             },
#             "output": "data/buffer_land.shp"
#         },
#         {
#             "name": "slope",
#             "inputs": {
#                 "tifffile": "data/terrain.tif"
#             },
#             "output": "data/slope.tif"
#         },
#         {
#             "name": "extractByValues",
#             "inputs": {
#                 "tifffile": "data/slope.tif",
#                 "min": 0,
#                 "max": 10
#             },
#             "output": "data/slope_10.tif"
#         },
#         {
#             "name": "polygon2mask",
#             "inputs": {
#                 "shpfile": "data/buffer_land.shp",
#                 "tiffile": "data/terrain.tif"
#             },
#             "output": "data/buffer_land_mask.tif"
#         },
#         {
#             "name": "rasterOverlay",
#             "inputs": {
#                 "datafile1": "data/slope_10.tif",
#                 "datafile2": "data/buffer_land_mask.tif"
#             },
#             "output": "data/slope_land.tif"
#         },
#         {
#             "name": "calculateArea",
#             "inputs": {
#                 "datafile": "data/slope_land.tif"
#             },
#             "output": "data/area_result"
#         }
#     ]
# """