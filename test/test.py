text = """
[\n  {\n    "name": "buffer",\n    "inputs": {\n      "datafile": "data/railway.shp",\n      "radius": "50"\n    },\n    "output": "data/temp/railway_buffer.shp"\n  },\n  {\n    "name": "slope",\n    "inputs": {\n      "tiffile": "data/terrain.tif"\n    },\n    "output": "data/temp/slope.tif"\n  },\n  {\n    "name": "overlay",\n    "inputs": {\n      "datafile1": "data/temp/slope.tif",\n      "datafile2": "data/farmland.shp"\n    },\n    "output": "data/temp/farmland_slope.tif"\n  },\n 
 {\n    "name": "area",\n    
    "inputs": {\n      "datafile": "data/temp/farmland_slope.tif",\n      
    "conditions": [\n        "slope<10",\n        "elevation<100"\n      ]
"""

import json
tools = json.loads(text)
print(tools)