# import tools
from tools.buffer import buffer
from tools.overlay import overlay
from tools.slope import slope
from tools.extractByValues import extractByValues
# from tools.extractByMask import extractByMask
# from tools.rasterOverlay import rasterOverlay
# from tools.polygon2mask import polygon2mask
from tools.area import area

# buffer("./data/railway.shp", 5000, "./data/buffer_railway.shp")
# overlay("./data/buffer_railway.shp", "./data/land.shp", "./data/overlay_buffer_land.shp")

# slope("./data/terrain.tif", "./data/slope_terrain.tif")
# extractByValues("./data/slope_terrain.tif", 0, 10, "./data/slope_values.tif")

# extractByValues("./data/terrain.tif", 0, 500, "./data/terrain_values.tif")

# rasterOverlay("./data/slope_values.tif","./data/terrain_values.tif", "./data/overlay_slope_terrain.tif")

# polygon2mask.polygon2mask("./data/overlay_buffer_land.shp", "./data/overlay_slope_terrain.tif", "./data/land_mask.tif")

# extractByMask("./data/overlay_slope_terrain.tif","./data/overlay_buffer_land.shp", "./data/result_land.tif")

print(area("./data/result_land.tif"))
