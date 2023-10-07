from gischain import init_gischain

# zhipuai的api_key，通过 http://open.bigmodel.cn/usercenter/apikeys 获取
glm_key = "293fd652b7deb69e82612e7edb07df3a.56KnrPvR3A14Eyu5"
# 通义千问的key，通过 https://dashscope.console.aliyun.com/apiKey 获取
qwen_key = "sk-f966cb8bbf914ec0b3dd3c1f771177fc"

# 用自然语言描述的指令，目前还需要带上数据文件的路径
instruction = "修一条铁路，宽度为50米，需要计算占用周边耕地的面积。数据文件都在data目录下，铁路是line.shp，耕地是region.shp。"

# 构造gischain，支持多种llm，某些llm需要给出key
chain = init_gischain(llm="chatglm", key=glm_key) 
# chain = init_gischain(llm="qwen-turbo", key=qwen_key) 

# 运行用户指令
output = chain.run(instruction)
print(f"最终的运行结果为：{output}")
