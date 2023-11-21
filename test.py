import json

obj = [{'farmland.shp': {'description': '耕地数据', 'fields': {'City': '地区名'}}}, {'railway.shp': {'description': '铁路数据'}}, {'terrain.tif': {'description': '地形数据'}}]
print(obj)

text = json.dumps(obj, ensure_ascii=False)

print(text)
