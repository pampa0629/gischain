"""
端到端验证脚本：不需要任何 LLM key。
通过 monkey-patch 把 llm.invoke 替换为返回硬编码的工具列表，
绕过真实调用，直接验证 check → execute → result 全链路。

用法：python mock_run.py
"""
import os
import sys
import warnings

warnings.simplefilter("once")

# base 环境的 fiona 损坏，强制走 pyogrio（与项目本身无关，仅为本地能跑）
os.environ.setdefault("config_file", "config.ini")
import geopandas as gpd
gpd.options.io_engine = "pyogrio"

from gischain.gischain import init_gischain


# 硬编码三段工具链：buffer → overlay → area
# 这是 check 修复后唯一被 check 通过的标准格式（平铺 parameters）
MOCK_TOOLS = [
    {
        "name": "buffer",
        "parameters": {
            "datafile": "data/railway.shp",
            "radius": 25,
            "output": "data/temp/railway_buffer.shp",
        },
    },
    {
        "name": "overlay",
        "parameters": {
            "datafile1": "data/temp/railway_buffer.shp",
            "datafile2": "data/farmland.shp",
            "output": "data/temp/overlay_result.shp",
        },
    },
    {
        "name": "area",
        "parameters": {
            "datafile": "data/temp/overlay_result.shp",
            "output": "data/output/area_result.json",
        },
    },
]


def main():
    if __name__ != "__main__":
        return

    # 准备目录
    os.makedirs("data/temp", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    # 清掉旧产物
    for p in (
        "data/temp/railway_buffer.shp",
        "data/temp/overlay_result.shp",
        "data/output/area_result.json",
    ):
        if os.path.exists(p):
            os.remove(p)

    print("=" * 60)
    print("Mock 模式：跳过真实 LLM 调用，直接验证修复后的链路")
    print("=" * 60)
    print("硬编码工具链：buffer(25m) → overlay → area\n")

    # 构造 gischain（key 给空串即可——我们会把 invoke monkey-patch 掉）
    chain = init_gischain(llm="chatglm", key="mock-key")

    # 关键：替换 invoke。select_data 要数据名 list，主流程要工具列表——根据 prompt 内容分流
    def mock_invoke(prompt, *args, **kwargs):
        if "选择数据" in prompt or "请你根据指令" in prompt:
            return ["farmland.shp", "railway.shp"]
        return MOCK_TOOLS

    chain.llm.invoke = mock_invoke
    # 同时替换 invoke_with_check 这条路径（如果存在的话）
    if hasattr(chain.llm, "invoke_and_check"):
        chain.llm.invoke_and_check = lambda *a, **kw: (True, MOCK_TOOLS, "")

    instruction = (
        "为 data/railway.shp 做 25 米缓冲区，"
        "与 data/farmland.shp 做相交分析，"
        "再统计相交部分的面积。"
    )

    print(f"指令: {instruction}\n")

    # show=False 避开可能的 pygraphviz 依赖问题（如果装了会自动显示）
    output = chain.run(instruction, show=False, multirun=False)

    # 检查 area_result.json 是否真的生成了
    result_path = "data/output/area_result.json"
    if os.path.exists(result_path):
        with open(result_path) as f:
            print(f"\n[SUCCESS] {result_path} 内容：")
            print(f.read())
    else:
        print(f"\n[FAIL] {result_path} 未生成")


if __name__ == "__main__":
    main()
