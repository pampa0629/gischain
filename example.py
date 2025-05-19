import os
# 这里要 config.ini 文件中的key值改为自己的key
os.environ["config_file"] = "config.ini"

import warnings
# 显示警告，但只显示一次
warnings.simplefilter("once")

from gischain.gischain import init_gischain

# 因为内部用了多进程，所以需要在main函数中调用
if __name__ == '__main__':

    # 铁路数据是railway.shp；耕地数据是farmland.shp,地区字段名为"City"；地形数据是terrain.tif。
    # 用自然语言描述的指令
    # instruction = "计算得到耕地面积。" # 
    instruction = "修一条铁路，宽度为50米，需要计算占用周边的耕地面积。" # 260654505.39415726
    # instruction = "修一条铁路，宽度为30米，需要计算占用周边坡度小于10度的耕地面积。" # 
    # instruction = "修一条铁路，宽度为50米，需要计算占用周边坡度小于10度、海拔小于100米的耕地面积。" # 46699805.60523755   
    # instruction = """修一条铁路，宽度为50米，需要计算占用周边坡度小于10度、海拔小于100米、位于“常德市” 城市内的耕地面积。""" # buffer半径25，面积：4225808.036933649
    # instruction = "修一条铁路，宽度为50米，需要分组统计所占用周边坡度小于10度、海拔小于100米、所属地区的耕地面积，并汇总到所属地区，从大到小的顺序进行排序。"
    
    # 构造gischain，支持多种llm，都需要给出key
    # chain = init_gischain(llm="chatglm", key=os.environ.get("glm_key")) # 
    chain = init_gischain(llm="qwen-turbo", key=os.environ.get("qwen_key"), funcall=False) # 提高很多
    # chain = init_gischain(llm="deepseek", key=os.environ.get("deepseek_key")) # 提高很多
    # chain = init_gischain(llm="ErnieBot4", key={"ak":os.environ.get("wenxin_ak"),"sk":os.environ.get("wenxin_sk")} ) # 
    # chain = init_gischain(llm="text2sql", key=os.environ.get("text2sql_key")) # 可以支持简单的指令
    # chain = init_gischain(llm="gpt3.5", key=os.environ.get("gpt_key")) # 可以支持第三档复杂的指令
    # chain = init_gischain(llm="gpt4", key=os.environ.get("gpt_key")) # 可以支持第三档复杂的指令

    # 运行用户指令，show=True表示显示工具执行的DAG图
    output = chain.run(instruction,show=True,multirun=False)
    
