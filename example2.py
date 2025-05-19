import os
# 这里要 config.ini 文件中的key值改为自己的key
os.environ["config_file"] = "config.ini"

import warnings
# 显示警告，但只显示一次
warnings.simplefilter("once")

from gischain.gischain import init_gischain

# 因为内部用了多进程，所以需要在main函数中调用
if __name__ == '__main__':

    # 用自然语言描述的指令 
    presume = "假定：步行五分钟能走300米，公园绿地类型的编码为1201,记得中间需要做数据融合。"
    instruction = presume + "计算南京市公园绿地步行五分钟的范围，占市区范围面积的比率。" 
    # 构造gischain，支持多种llm，都需要给出key
    # chain = init_gischain(llm="chatglm", key=os.environ.get("glm_key")) # 
    chain = init_gischain(llm="qwen-turbo", key=os.environ.get("qwen_key"), funcall=True) # 提高很多
    # chain = init_gischain(llm="deepseek", key=os.environ.get("deepseek_key")) # 提高很多
    # chain = init_gischain(llm="ErnieBot4", key={"ak":os.environ.get("wenxin_ak"),"sk":os.environ.get("wenxin_sk")} ) # 
    # chain = init_gischain(llm="text2sql", key=os.environ.get("text2sql_key")) # 可以支持简单的指令
    # chain = init_gischain(llm="gpt3.5", key=os.environ.get("gpt_key")) # 可以支持第三档复杂的指令
    # chain = init_gischain(llm="gpt4", key=os.environ.get("gpt_key")) # 可以支持第三档复杂的指令

    # 运行用户指令，show=True表示显示工具执行的DAG图
    output = chain.run(instruction,show=True,multirun=False)
    
