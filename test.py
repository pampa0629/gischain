import matplotlib.pyplot as plt

# 创建一个简单的图形
fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(111)

# 关闭横轴和纵轴
ax.set_axis_off()


# 绘制一些数据（这里只是举例）
data = [1, 2, 3, 4, 5]
ax.plot(data)



# 显示图形
plt.show()
