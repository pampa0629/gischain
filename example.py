from gischain.gischain import init_gischain

import os
# 设置禁用文件验证的环境变量
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

# zhipuai的api_key，通过 http://open.bigmodel.cn/usercenter/apikeys 获取
glm_key = "293fd652b7deb69e82612e7edb07df3a.56KnrPvR3A14Eyu5"
# 通义千问的key，通过 https://dashscope.console.aliyun.com/apiKey 获取
qwen_key = "sk-f966cb8bbf914ec0b3dd3c1f771177fc"
# 文心一言，需要ak和sk
# 通过 https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application/create 获取
wenxin_ak = "Gev6k0qO9OPatIHCu41iCKAS"
wenxin_sk = "M6GqjYAVygDm7Fqee1ENZQ9KEpk4a8Qh"    
# text2sql的key
text2sql_key = "MjBlODExNTQ5ZjVlYWFjMGM3NTQ1Y2RkMzJlNTBjNDYwZDc2ODM3OA=="
# gpt4的key，通过 https://console.closeai-asia.com/ 获取
gpt_key = 'sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm'

# 因为内部用了多进程，所以需要在main函数中调用
if __name__ == '__main__':

    # 用自然语言描述的指令，目前还需要带上数据文件的路径
    instruction = "修一条铁路，宽度为50米，需要计算占用周边的耕地面积。铁路数据是railway.shp，耕地数据是land.shp。"
    # instruction = "修一条铁路，宽度为50米，需要计算占用周边坡度小于10度的耕地面积。铁路是railway.shp，耕地是land.shp，地形数据是terrain.tif。"

    # 构造gischain，支持多种llm，基本都需要给出key
    # chain = init_gischain(llm="chatglm", key=glm_key) # 可以支持简单的指令
    # chain = init_gischain(llm="qwen-turbo", key=qwen_key) # 简单的都会出错
    # chain = init_gischain(llm="ErnieBot4", key={"ak":wenxin_ak,"sk":wenxin_sk} ) # 可以支持简单的指令
    # chain = init_gischain(llm="text2sql", key=text2sql_key) # 简单的都会出错
    chain = init_gischain(llm="gpt4", key=gpt_key) # 可以支持复杂的指令

    # 运行用户指令，show=True表示显示工具执行的DAG图
    output = chain.run(instruction,show=True,multirun=True)
    print(f"最终的运行结果为：{output}")
