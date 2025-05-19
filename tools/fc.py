#把function call中的基础函数，都放在这里来定义
# 根据name、description、parameters生成工具描述
def build_fc_core(name, description, parameters):
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": parameters
        }
    }

# 外面在多包一下壳，给function call用的
def build_fc_obj(core_obj):
    return {
        "type": "function",
        "function": core_obj
    }