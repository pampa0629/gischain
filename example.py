from gischain import init_gischain

# key为zhipuai的api_key，通过 http://open.bigmodel.cn/usercenter/apikeys 获取
key = "293fd652b7deb69e82612e7edb07df3a.56KnrPvR3A14Eyu5"

# 用自然语言描述的指令，目前还需要带上数据文件的路径
instruction = "修一条铁路，宽度为50米，需要计算占用周边耕地的面积。数据文件都在data目录下，铁路是line.shp，耕地是region.shp。"

# llm="chatglm" 目前只支持chatglm
chain = init_gischain(key=key) 
output = chain.run(instruction)
print(f"最终的运行结果为：{output}")
