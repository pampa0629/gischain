import json

text = """{"farmland.shp": {"description": "耕地数据", "fields": {"City": "地区名"}}}, {"terrain.tif": {"description": "地形数据"}}"""

text2 = "["+text+"]"
print(text2)

objs = json.loads(text2)

names = [list(obj.keys())[0] for obj in objs]
# names = []

# for obj in objs:
#     print(obj)
#     print(obj.keys())
#     names.append(list(obj.keys())[0])


print(names)
