desc = """{
    "name":"sort",
    "description":"根据指定字段的属性值进行排序",
    "inputs":{
        "datafile":"要进行排序的数据文件，支持cvs和json格式",
        "field":"要进行排序的字段名",
        "mode":"排序方式，包括asc（升序）、desc（降序）等"
    },
    "output":"输出的排序后的数据文件，支持cvs和json格式"
}
"""

example = """
指令：对不同地区的耕地面积进行从大到小进行排序；耕地数据是 farmland.csv，面积字段是“Area”。
json: [{
	"name":"sort",
	"inputs":{
		"datafile":"farmland.csv",
		"field":"Area",
        "mode":"desc"
    },
    "output":"farmland_sort.csv"
}]
"""

def check(tool):
    datafile = tool["inputs"]["datafile"]
    # 必须是shape、csv、json等格式
    if not datafile.endswith(".csv") and not datafile.endswith(".json"):
        return False, f"对于工具{tool['name']}，输入的datafile参数必须是csv或json文件，而不能是{datafile}；"
    return True, ""

from . import base
import pandas as pd

def sort(datafile, field, mode, output):
    df = base.read_dataframe(datafile)

    if mode == 'asc':
        result = df.sort_values(by=field, ascending=True)
    elif mode == 'desc':
        result = df.sort_values(by=field, ascending=False)
    # print(result)

    base.write_dataframe(result, output)
    return output