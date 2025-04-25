     
def module_init():    
    from . import config
    import os
    if "config_file" in os.environ:
        config.load_config(os.environ["config_file"])
    else:
        print("没有找到环境变量 config_file，使用默认的配置文件 config.ini")
        os.environ["config_file"] = "config.ini"
        config.load_config(os.environ["config_file"])

    from . import define
    from . import area, buffer, filter, dissolve, overlay,slope,extractByValues,rasterStatistics,groupStatistics,sort,ratio
    
    define.add_tool("area", area.area, area.desc, area.example, area.check)
    define.add_tool("buffer", buffer.buffer, buffer.desc, buffer.example, buffer.check)
    define.add_tool("filter", filter.filter, filter.desc, filter.example, filter.check)
    define.add_tool("dissolve", dissolve.dissolve, dissolve.desc, dissolve.example, dissolve.check)
    define.add_tool("slope", slope.slope, slope.desc, slope.example, slope.check)
    define.add_tool("overlay", overlay.overlay, overlay.desc, overlay.example, overlay.check)
    define.add_tool("extractByValues", extractByValues.extractByValues, extractByValues.desc, extractByValues.example, extractByValues.check)

    define.add_tool("rasterStatistics", rasterStatistics.rasterStatistics, rasterStatistics.desc, rasterStatistics.example, rasterStatistics.check)
    define.add_tool("groupStatistics", groupStatistics.groupStatistics, groupStatistics.desc, groupStatistics.example, groupStatistics.check)
    define.add_tool("sort", sort.sort, sort.desc, sort.example, sort.check)

    define.add_tool("ratio", ratio.ratio, ratio.desc, ratio.example)

    # 效果不好，暂时封起来
    # from . import polygon2mask,contourPolygon
    # define.add_tool("polygon2mask", polygon2mask.polygon2mask, polygon2mask.desc, polygon2mask.example)
    # define.add_tool("contourPolygon", contourPolygon.contourPolygon, contourPolygon.desc,contourPolygon.example)
    
# 在模块加载时自动调用 module_init() 函数
module_init()

