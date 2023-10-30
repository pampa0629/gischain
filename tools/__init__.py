from . import area, buffer, define, overlay,slope,extractByValues,polygon2mask,contourPolygon
     
def module_init():    
    define.add_tool("area", area.area, area.desc, area.example)
    define.add_tool("buffer", buffer.buffer, buffer.desc, buffer.example)
    define.add_tool("slope", slope.slope, slope.desc, slope.example)
    define.add_tool("overlay", overlay.overlay, overlay.desc, overlay.example)
    define.add_tool("extractByValues", extractByValues.extractByValues, extractByValues.desc, extractByValues.example)

    # 效果不好，暂时封起来
    # define.add_tool("polygon2mask", polygon2mask.polygon2mask, polygon2mask.desc, polygon2mask.example)
    # define.add_tool("contourPolygon", contourPolygon.contourPolygon, contourPolygon.desc,contourPolygon.example)

    # 初始化 tools 的 embedding
    define.init_tools_emb()
    
# 在模块加载时自动调用 module_init() 函数
module_init()

