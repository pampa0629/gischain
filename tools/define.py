# from tools import buffer,overlay,calculateArea

tools_mapping = {
    # "buffer": {"func":buffer,"dics":},
    # "overlay": overlay,
    # "calculateArea": calculateArea,
}

def call_tool(name, **kwargs):
    if name in tools_mapping:
        func = tools_mapping[name]["func"]
        print("call_tool:",name,kwargs)
        return func(**kwargs)
    else:
        print("Function not found")
        return None

def add_tool(name, func, disc):
    tools_mapping[name] = {}
    tools_mapping[name]["func"] = func
    tools_mapping[name]["disc"] = disc
    print("add_tool:",tools_mapping[name])

def get_tool_disc(name):
    if name in tools_mapping:
        function = tools_mapping[name]
        return function["disc"]
    else:
        print("Function not found")
        return None
    
def get_tools_name():
    return list(tools_mapping.keys())