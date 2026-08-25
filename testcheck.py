# testcheck.py — 验证 check.check_tools 纠错逻辑（不需要真实的大模型API）
import os
import json

# 定位到项目根目录下的 config.ini（真实存在的那个），避免加载不存在的 myconfig.ini
script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["config_file"] = os.path.join(script_dir, "config.ini")

from gischain import check

instruction = "修一条铁路，宽度为50米，需要计算占用周边的耕地面积。"
data_descs = '{"farmland.shp": {"description": "耕地数据", "fields": {"City": "地区名"}}},{"railway.shp": {"description": "铁路数据"}}'

passed = 0
failed = 0

def run_case(case_name, tools, expect_ok):
    global passed, failed
    ok, errors = check.check_tools(tools, instruction, data_descs)
    status = "PASS" if ok == expect_ok else "FAIL"
    if ok == expect_ok:
        passed += 1
    else:
        failed += 1
    print(f"[{status}] {case_name}: ok={ok}")
    if errors:
        print(f"        errors: {errors[:200]}")
    return ok, errors

# ---------- 用例1：旧版 inputs/output 格式，逻辑正确 ----------
# 模拟LLM照着旧few-shot范例输出的格式，应被归一化后通过检查
tools_old_format = [
    {"name": "buffer", "inputs": {"datafile": "data/railway.shp", "radius": 25}, "output": "data/temp/railway_buffer.shp"},
    {"name": "overlay", "inputs": {"datafile1": "data/temp/railway_buffer.shp", "datafile2": "data/farmland.shp"}, "output": "data/temp/overlay_result.shp"},
    {"name": "area", "inputs": {"datafile": "data/temp/overlay_result.shp"}, "output": "data/output/area_result.json"},
]
ok, _ = run_case("旧格式(inputs/output)+逻辑正确", tools_old_format, True)
assert ok and "parameters" in tools_old_format[0] and "output" in tools_old_format[0]["parameters"], "应被归一化为parameters格式"
print(f"        归一化后第1个工具: {json.dumps(tools_old_format[0], ensure_ascii=False)}")

# ---------- 用例2：新版 parameters 格式，逻辑正确 ----------
tools_new_format = [
    {"name": "buffer", "parameters": {"datafile": "data/railway.shp", "radius": 25, "output": "data/temp/railway_buffer.shp"}},
    {"name": "overlay", "parameters": {"datafile1": "data/temp/railway_buffer.shp", "datafile2": "data/farmland.shp", "output": "data/temp/overlay_result.shp"}},
    {"name": "area", "parameters": {"datafile": "data/temp/overlay_result.shp", "output": "data/output/area_result.json"}},
]
run_case("新格式(parameters平铺)+逻辑正确", tools_new_format, True)

# ---------- 用例2b：v0.1.8迁移残留的嵌套格式(parameters.inputs)，应被归一化后通过 ----------
tools_nested_format = [
    {"name": "buffer", "parameters": {"inputs": {"datafile": "data/railway.shp", "radius": 25}, "output": "data/temp/railway_buffer.shp"}},
    {"name": "overlay", "parameters": {"inputs": {"datafile1": "data/temp/railway_buffer.shp", "datafile2": "data/farmland.shp"}, "output": "data/temp/overlay_result.shp"}},
    {"name": "area", "parameters": {"inputs": {"datafile": "data/temp/overlay_result.shp"}, "output": "data/output/area_result.json"}},
]
ok, _ = run_case("嵌套格式(parameters.inputs)+逻辑正确", tools_nested_format, True)
assert ok and tools_nested_format[0]["parameters"].get("datafile") == "data/railway.shp", "嵌套格式应被归一化为平铺parameters"
print(f"        归一化后第1个工具: {json.dumps(tools_nested_format[0], ensure_ascii=False)}")

# ---------- 用例3：臆造了数据来源中不存在的文件 ----------
tools_fake_file = [
    {"name": "buffer", "parameters": {"datafile": "data/land.shp", "radius": 25, "output": "data/temp/land_buffer.shp"}},
    {"name": "area", "parameters": {"datafile": "data/temp/land_buffer.shp", "output": "data/output/area_result.json"}},
]
run_case("臆造文件(data/land.shp)", tools_fake_file, False)

# ---------- 用例4：中间数据生成了但没有被后续使用 ----------
tools_unused_temp = [
    {"name": "buffer", "parameters": {"datafile": "data/railway.shp", "radius": 25, "output": "data/temp/railway_buffer.shp"}},
    {"name": "area", "parameters": {"datafile": "data/farmland.shp", "output": "data/output/area_result.json"}},
]
run_case("中间数据未被使用", tools_unused_temp, False)

# ---------- 用例5：第一个工具输入的文件在磁盘上不存在 ----------
tools_missing_file = [
    {"name": "buffer", "parameters": {"datafile": "data/railway_notexist.shp", "radius": 25, "output": "data/temp/railway_buffer.shp"}},
    {"name": "area", "parameters": {"datafile": "data/temp/railway_buffer.shp", "output": "data/output/area_result.json"}},
]
run_case("文件不存在", tools_missing_file, False)

# ---------- 用例6：异常输入不崩溃 ----------
run_case("tools为None", None, False)
run_case("tools为空列表", [], False)
run_case("工具结构不完整(缺output)", [{"name": "buffer", "parameters": {"datafile": "data/railway.shp", "radius": 25}}], False)
run_case("混合格式(output在顶层)", [{"name": "buffer", "parameters": {"datafile": "data/railway.shp", "radius": 25}, "output": "data/temp/railway_buffer.shp"},
                                      {"name": "area", "parameters": {"datafile": "data/temp/railway_buffer.shp", "output": "data/output/area_result.json"}}], True)

print("\n" + "=" * 60)
print(f"测试完成：通过 {passed} 个，失败 {failed} 个")
exit(0 if failed == 0 else 1)
