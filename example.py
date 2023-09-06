from gischain import init_gischain

# tools = ["","",""]

instruction = "修一条铁路，宽度为50米，需要计算占用周边耕地的面积。数据文件都在data目录下，铁路是line.shp，耕地是region.shp。"

chain = init_gischain() # ,tools=tools) llm="chatglm"
output = chain.run(instruction)
print(output)