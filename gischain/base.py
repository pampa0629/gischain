# 基础能力放到这里，避免依赖关系混乱
import re, os
import json

# 按照结果类型，以合理的方式打印出来，包括：shapefile, tif, json, txt, csv，数值等
def print_everything(value):
    if isinstance(value, str):
        if os.path.isfile(value):
            _, ext = os.path.splitext(value)
            if ext == ".shp":
                import geopandas as gpd
                gdf = gpd.read_file(value)
                print(gdf)
            elif ext == ".tif" or ext == ".tiff":
                import rasterio
                with rasterio.open(value) as src:
                    print(src.profile)
            elif ext == ".json":
                with open(value) as f:
                    print(json.load(f))
            elif ext == ".txt" or ext == ".csv":
                with open(value) as f:
                    print(f.read())
            else:
                print(value)
        else:
            print(value)
    elif isinstance(value, dict):
        print(json.dumps(value, indent=4, ensure_ascii=False))
    elif isinstance(value, list):
        print(json.dumps(value, indent=4, ensure_ascii=False))
    elif isinstance(value, int) or isinstance(value, float):
        print(value)
    elif isinstance(value, tuple):
        print(value)
    else:
        print("不支持的结果类型")

def get_base_filename(filename):
    if is_valid_file_path(filename):
        return os.path.basename(filename)
    return filename

# 判断text是否是数值型
def is_numeric(text):
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return bool(re.match(pattern, text))

# 判断 file_path 是否是合法的文件路径
def is_valid_file_path(file_path):
    # 使用 os.path 模块中的函数检查路径是否合法
    return os.path.dirname(file_path) != '' and os.path.basename(file_path) != ''

# 判断tool中，input 是否准备就绪; 就绪返回"ready",否则返回"noready"
# 如果是数值型、字符串类型，则直接OK；如果是文件型，则判断文件是否存在
def input_ready_status(key, value):
    if isinstance(value, (int, float)) or is_numeric(value):
        return "ready"
    elif isinstance(value, str): # 如果是字符串
        # 如果是文件路径，则判断文件是否存在
        if is_valid_file_path(value) and os.path.isfile(value):
            return "ready"
        # 不是文件路径，则直接OK
        elif is_valid_file_path(value) == False:
            return "ready"
    # 其他情况，都返回 noready
    return "noready"
    
# 眼色映射字典
node_color_map = {
    # R G B
    ("task", "todo"):  "lightblue", # 浅蓝色
    # ("task", "ready"): "turquoise", # 绿松石色
    ("task", "doing"): "violet", # 紫罗兰色
    ("task", "done"):  "gold", # 金色
    
    ("data", "noready"): "teal", # 蓝绿色
    ("data", "ready"): "lightgreen", # 浅蓝色
}

# share 的数据结构
# { node_name1:
#       {‘type’:'task', # 或者是 data
#       'label':'buffer', # 或者是文件名
#       'shape':'hexagon', # 或者是ellipse
#        'status':'todo', # 或者是 doing 或者是 done
#        'tool':'buffer', 
#        'color':'lightblue', 
#        'result':filepath },
#   node_name2:{}, ...}
# 对于edge, 用tuple表示key，如：(node_name1, node_name2)
# 增加 title, 表示"执行状态"

# 以json格式打印shares
def print_shares(shares):
    for key, value in shares.items():
        print(f"key={key}, value={value}")

# 判断是否为node
def is_node(key,shares):
    if isinstance(key, str) and key in shares and 'type' in shares[key]:
        return True
    return False

# 判断是否为edge
def is_edge(key,shares):
    if isinstance(key, tuple) and key in shares:
        return True
    return False
    
# 从 tools 中共享变量
def buildShares(tools):
    # 用于多进程共享变量
    import multiprocessing
    manager = multiprocessing.Manager()
    shares = manager.dict()
    # title
    shares.update({"title":"GISChain is Running ......"})
    # 定义task和data的形状
    task_shape = 'box' # hexagon
    data_shape = 'ellipse'

    # 添加任务和其输入输出到图中
    for tool in tools:
        tool_name = tool["name"]
        # 这里要把tool的全部信息合并为一个字符串作为task的名字，否则会出现重名的情况
        task_name = json.dumps(tool) 

        # task 节点增加status属性，包括以下状态：
        #   todo  尚未处理，等到所有inputs都准备好后，就可以开始执行
        #   doing 正在执行中
        #   done  执行完毕
        shares.update({task_name: {"tool":tool_name, "label":tool_name, "type":'task', "shape":task_shape,"status":'todo', "color":node_color_map.get(('task', 'todo'))}})
        
        # data 节点增加status属性，包括以下状态：
        #   noready  尚未准备好，等待上游task的输出
        #   ready 已经准备好，可以为后续task使用
        inputs = tool["inputs"]
        for key,value in inputs.items():
            status = input_ready_status(key, value)
            value = str(value) # 转换为字符串，避免出现数字型的key
            label = get_base_filename(value) # 只保留文件名，去掉路径
            shares.update({value: {"label":label, "type":'data',  "shape":data_shape,"status":status, "color":node_color_map.get(('data', status))}})
            # 对于 edge，用tuple表示key，如：(node_name1, node_name2)
            shares.update({(value, task_name):{}})
            
        output = tool["output"]
        label = get_base_filename(output) # 只保留文件名，去掉路径
        shares.update({output: {"label":label, "type":'data',"shape":data_shape,"status":'noready', "color":node_color_map.get(('data', 'noready'))}})
        # 对于 edge，用tuple表示key，如：(node_name1, node_name2)
        shares.update({(task_name, output):{}})

    return shares

# 通过shares还原DAG
def resotreDAG(shares):
    import pygraphviz as pgv
    G = pgv.AGraph(directed=True)
    for key,value in shares.items():
        if is_node(key,shares):
            G.add_node(key, label=value['label'], shape=value['shape'], color=value['color'])
        elif is_edge(key,shares): 
            G.add_edge(key[0], key[1])
    return G

# 只修改部分属性，其他的仍然要保留
def update_kv_dict(shares, name, kv_dict):
    node_data = shares[name]
    node_data.update(kv_dict)
    shares.update({name: node_data})
