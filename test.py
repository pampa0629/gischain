# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus

import dashscope # import Generation

# export DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
# 模型服务API Key: sk-f966cb8bbf914ec0b3dd3c1f771177fc
dashscope.api_key="sk-f966cb8bbf914ec0b3dd3c1f771177fc"

def sample_sync_call():
    prompt_text="""
你现在是一个人工智能助手，现在要做一个gis领域的空间分析功能。
你需要按照给出的要求完成任务，从下面工具集中选择合适的工具(不要选用不上的工具)，
并用JSON格式顺序列出对应的工具，请给出对应的输入信息，记得组合出完整的文件路径名。
由于要对接程序自动运行，不要有任何多余的文字输出，多余的文字都是干扰项。
要求：修一条铁路，宽度为50米，需要计算占用周边耕地的面积。数据文件都在data目录下，铁路是line.shp，耕地是region.shp。
工具集如下：
{
    name:buffer,
    discription:得到缓冲区,
    inputs:{
        datafile:要求缓冲区的数据文件
        radius:缓冲区半径
    },
    output:缓冲区结果文件
}
{
    name:overlay,
    discription:叠加分析,
    inputs:{
        datafile1:参与叠加分析的数据文件1,
        datafile2:参与叠加分析的数据文件2
    },
    output:叠加分析结果文件
}
{
    name:calculateArea,
    discription:计算面积，并求和,
    inputs:{
        datafile:要求面积的数据文件
    },
    output:面积结果
}
==========
"""
    resp=dashscope.Generation.call(
        model='qwen-turbo',
        prompt=prompt_text
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if resp.status_code == HTTPStatus.OK: 
        print(resp.output) # The output text
        print(resp.usage)  # The usage information
    else:
        print(resp.code) # The error code.
        print(resp.message) # The error message.

sample_sync_call()