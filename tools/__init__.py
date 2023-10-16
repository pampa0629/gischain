from . import buffer, define, overlay,calculateArea,slope,extractByMask,extractByValues,rasterOverlay,polygon2mask

def module_init():
    define.add_tool("buffer", buffer.buffer, buffer.disc)
    define.add_tool("overlay", overlay.overlay, overlay.disc)
    define.add_tool("calculateArea", calculateArea.calculateArea, calculateArea.disc)
    define.add_tool("slope", slope.slope, slope.disc)

    define.add_tool("extractByMask", extractByMask.extractByMask, extractByMask.disc)
    define.add_tool("extractByValues", extractByValues.extractByValues, extractByValues.disc)
    define.add_tool("rasterOverlay", rasterOverlay.rasterOverlay, rasterOverlay.disc)
    define.add_tool("polygon2mask", polygon2mask.polygon2mask, polygon2mask.disc)
    # 效果不好，暂时封起来
    # define.add_tool("contourPolygon", contourPolygon.contourPolygon, contourPolygon.disc)

# 在模块加载时自动调用 module_init() 函数
module_init()
