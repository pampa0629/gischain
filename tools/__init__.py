from . import buffer,overlay,calculateArea,define

def module_init():
    define.add_tool("buffer", buffer.buffer, buffer.disc)
    define.add_tool("overlay", overlay.overlay, overlay.disc)
    define.add_tool("calculateArea", calculateArea.calculateArea, calculateArea.disc)

# 在模块加载时自动调用 module_init() 函数
module_init()
