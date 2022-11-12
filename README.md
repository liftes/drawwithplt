# PythonDraw
提供了科研绘图的常用功能的封装。

包括：
字体统一设置：中文显示和字体字号设置，中文宋体，西文新罗马；

颜色统一设置：利用cmap色卡，返回colorlist；

快捷保存图片：统一dpi=600；并设置bool值方便统一控制是否保存。

热力图绘制：等高线，坐标轴矫正

3D图绘制：等高线和投影

样条插值等……

# 使用方法
将Draw.py文件放入工作目录；
```python
# 导入必要的绘图库
from Draw import plt,sns
import Draw as D

# 设置色卡
color_list = D.SetColor('tab20',np.linspace(0, 1, 10))

# 使用热力图绘制的字典控制及代码示例：
xdict = {"name": "ylabel", "step": 5,"start":1, "fmt":"%.0f"}
ydict = {"name": "xlabel", "step": 5, "angle":0, "fmt":"%.0f"}
zdict = {"name": "Random"}
x = np.array(range(32))
y = np.array(range(32))
z = np.random.randint(0,10,(32,32))
D.snsFix(x, y, z, xl=xdict, yl=ydict, zl=zdict,
         normalZero=True, contour=False)
```

## 更新：（2022-4-30）
提供了自定义默认参数的快捷入口，提供了自定义渐变颜色及色卡展示，完善了热力图的绘制模块，对colorbar开放了自定义设置接口

## 配色网站参考
https://color.uisdc.com/pick.html
